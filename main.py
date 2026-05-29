from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import yt_dlp

class DescargadorHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/descargar':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            tweet_url = data.get('url')

            # Configuración directa para bajar el video a tu PC
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': '%(title)s_%(id)s.%(ext)s',
                'quiet': True
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([tweet_url])
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

# Levantar el servidor en el puerto 8000
print("Servidor corriendo en http://localhost:8000")
server = HTTPServer(('localhost', 8000), DescargadorHandler)
server.serve_forever()