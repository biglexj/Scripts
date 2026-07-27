# 🚀 Guía de Auto-Actualización Directa desde GitHub (Android & KMP)

Esta guía explica cómo implementar en cualquier proyecto (Android nativo o Kotlin Multiplatform) la funcionalidad de comprobar actualizaciones automáticamente desde **GitHub Releases**, descargar la última versión de la APK en segundo plano usando `DownloadManager` y solicitar al usuario la instalación con un solo clic.

---

## 🛠️ Estructura del Componente

### 1. Modelo de Datos (`UpdateRelease.kt`)

```kotlin
data class UpdateRelease(
    val version: String,
    val downloadUrl: String,
    val releasePageUrl: String,
    val body: String = ""
)
```

---

### 2. Parseador y Verificador (`UpdateChecker.kt`)

```kotlin
object UpdateChecker {
    private fun extractStringValue(json: String, key: String): String? {
        val search = "\"$key\":"
        val keyIndex = json.indexOf(search)
        if (keyIndex == -1) return null
        val start = json.indexOf("\"", keyIndex + search.length)
        if (start == -1) return null
        val end = json.indexOf("\"", start + 1)
        if (end == -1) return null
        return json.substring(start + 1, end)
    }

    fun parseUpdateRelease(json: String): UpdateRelease? {
        val tagName = extractStringValue(json, "tag_name") ?: return null
        val htmlUrl = extractStringValue(json, "html_url") ?: return null
        val body = extractStringValue(json, "body").orEmpty()

        val apkIndex = json.indexOf(".apk\"")
        val downloadUrl = if (apkIndex != -1) {
            val assetsRegion = json.substring(0, apkIndex)
            val downloadKeySearch = "\"browser_download_url\":"
            val downloadKeyIndex = assetsRegion.lastIndexOf(downloadKeySearch)
            if (downloadKeyIndex != -1) {
                val start = assetsRegion.indexOf("\"", downloadKeyIndex + downloadKeySearch.length)
                if (start != -1) {
                    val end = json.indexOf("\"", start + 1)
                    if (end != -1) json.substring(start + 1, end) else htmlUrl
                } else htmlUrl
            } else htmlUrl
        } else htmlUrl

        val cleanVersion = tagName.removePrefix("v").trim()
        return UpdateRelease(
            version = cleanVersion,
            downloadUrl = downloadUrl,
            releasePageUrl = htmlUrl,
            body = body
        )
    }

    fun isNewerVersion(current: String, remote: String): Boolean {
        val currentParts = current.split(".").mapNotNull { it.takeWhile { c -> c.isDigit() }.toIntOrNull() }
        val remoteParts = remote.split(".").mapNotNull { it.takeWhile { c -> c.isDigit() }.toIntOrNull() }
        val maxLen = maxOf(currentParts.size, remoteParts.size)
        for (i in 0 until maxLen) {
            val c = currentParts.getOrElse(i) { 0 }
            val r = remoteParts.getOrElse(i) { 0 }
            if (r > c) return true
            if (c > r) return false
        }
        return false
    }
}
```

---

### 3. Petición a la API de GitHub

```kotlin
suspend fun fetchLatestRelease(owner: String, repo: String): UpdateRelease? = withContext(Dispatchers.IO) {
    runCatching {
        val url = java.net.URL("https://api.github.com/repos/$owner/$repo/releases/latest")
        val connection = url.openConnection() as java.net.HttpURLConnection
        connection.requestMethod = "GET"
        connection.connectTimeout = 10_000
        connection.readTimeout = 10_000
        connection.setRequestProperty("User-Agent", "$repo-App-Updater")
        if (connection.responseCode == 200) {
            val json = connection.inputStream.bufferedReader().use { it.readText() }
            UpdateChecker.parseUpdateRelease(json)
        } else null
    }.getOrNull()
}
```

---

### 4. Descargar e Iniciar Instalación en Android (`DownloadManager`)

```kotlin
fun downloadAndInstallApk(context: Context, release: UpdateRelease, appName: String) {
    if (release.downloadUrl.endsWith(".apk", ignoreCase = true)) {
        val dm = context.getSystemService(Context.DOWNLOAD_SERVICE) as? DownloadManager
        if (dm != null) {
            val request = DownloadManager.Request(Uri.parse(release.downloadUrl)).apply {
                setTitle("Descargando $appName v${release.version}")
                setDescription("Nueva actualización disponible")
                setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                setDestinationInExternalPublicDir(
                    Environment.DIRECTORY_DOWNLOADS,
                    "$appName-v${release.version}.apk"
                )
                setMimeType("application/vnd.android.package-archive")
            }
            dm.enqueue(request)
            return
        }
    }
    // Si no es un APK o falla DownloadManager, abrir en el navegador
    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(release.releasePageUrl)).apply {
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    }
    context.startActivity(intent)
}
```

---

## 📌 Permisos Necesarios en `AndroidManifest.xml`

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />
```

> **Nota**: Para Android 8.0 (API 26) o superior, el usuario deberá conceder permiso a la aplicación para instalar aplicaciones desconocidas si descarga fuera de Google Play.

---

## 📝 Resumen del Flujo de Trabajo

1. Al abrir la app, ejecuta `checkSilent()` — verificación en background sin feedback visible.
2. Compara `UpdateChecker.isNewerVersion(currentVersion, release.version)`.
3. Si hay una versión superior, muestra el `UpdateBanner` flotante.
4. Si el usuario pulsa "Buscar actualizaciones" manualmente y ya está al día, muestra el toast global ✅ 4 s.
5. Al hacer clic en "Actualizar", llama a `downloadAndInstallApk(context, release, appName)`.

---

### 5. Sanitización del `body` de GitHub Releases

> [!IMPORTANT]
> El campo `body` de la API de GitHub contiene **Markdown crudo** con `\r\n`, `**negrita**`, `## Títulos`, backticks, etc. Siempre sanitizarlo antes de mostrarlo en la UI.

```kotlin
/** Elimina sintaxis Markdown básica y saltos de línea para mostrar texto limpio en la UI. */
fun sanitizeMarkdown(text: String): String =
    text
        .replace(Regex("\\*{1,3}(.+?)\\*{1,3}"), "$1")  // negrita / cursiva → texto plano
        .replace(Regex("#{1,6}\\s*"), "")                 // ## Encabezados → eliminar
        .replace(Regex("`{1,3}[^`]*`{1,3}"), "")          // `código` / ```bloque``` → eliminar
        .replace(Regex("-\\s+"), "• ")                    // - listas → bullet
        .replace(Regex("\\r\\n|\\n\\r|\\r"), " ")         // saltos de línea CRLF/CR → espacio
        .replace("\n", " ")                               // saltos de línea LF → espacio
        .replace(Regex(" {2,}"), " ")                     // espacios múltiples → uno
        .trim()
```

**Uso en `UpdateBanner`:**

```kotlin
val bodyText = release.body
    .let { sanitizeMarkdown(it) }
    .ifBlank { "Hay una versión más reciente con mejoras de rendimiento y correcciones." }

Text(
    text = bodyText,
    style = MaterialTheme.typography.bodySmall,
    maxLines = 2,
    overflow = TextOverflow.Ellipsis,
)
```

---

### 6. Toast Global "Estás al día" (KMP Desktop / Multiplatform)

Cuando la verificación manual **no** encuentra una versión nueva, mostrar un toast flotante sobre toda la UI con auto-dismiss de 4 segundos:

```kotlin
// En el ViewModel / estado raíz:
var upToDate by remember { mutableStateOf(false) }

// Auto-dismiss tras 4 s:
LaunchedEffect(upToDate) {
    if (upToDate) {
        delay(4_000)
        upToDate = false
    }
}

// Overlay en la raíz del árbol (dentro de Box que cubre toda la pantalla):
AnimatedVisibility(
    visible = upToDate,
    modifier = Modifier
        .align(Alignment.TopCenter)
        .padding(top = 16.dp),
    enter = fadeIn() + slideInVertically { -it },
    exit  = fadeOut() + slideOutVertically { -it },
) {
    Card(
        shape = MaterialTheme.shapes.medium,
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.secondaryContainer,
            contentColor   = MaterialTheme.colorScheme.onSecondaryContainer,
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 6.dp),
    ) {
        Text(
            text = "✅ Estás en la última versión de LyraFlow.",
            style = MaterialTheme.typography.bodyMedium,
            modifier = Modifier.padding(horizontal = 20.dp, vertical = 12.dp),
        )
    }
}
```

> [!TIP]
> Coloca el `AnimatedVisibility` **fuera** de cualquier `ScrollableColumn` o pantalla específica, directamente en el `Box` raíz de `Surface`, para que el toast sea visible sin importar en qué pantalla esté el usuario.

---

### 7. Separar Check Silencioso del Check Manual

```kotlin
// Silencioso al iniciar — sin feedback si ya está al día:
val checkSilent: suspend () -> Unit = {
    val release = updateService.checkLatestRelease()
    if (release != null && UpdateChecker.isNewerVersion(currentVersion, release.version)) {
        availableUpdate = release
    }
}

// Manual — siempre informa el resultado:
val checkForUpdates: () -> Unit = {
    upToDate = false
    scope.launch {
        val release = updateService.checkLatestRelease()
        if (release != null && UpdateChecker.isNewerVersion(currentVersion, release.version)) {
            availableUpdate = release
            upToDate = false
        } else {
            upToDate = true  // activa el toast global
        }
    }
}

LaunchedEffect(Unit) { checkSilent() }
```
