# modules/media_processor.py
"""
Processador Avançado de Mídia
Integra capacidades de geração, refinamento e análise de mídia
"""

import os
import json
import requests
import base64
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
import speech_recognition as sr
import pyttsx3

class ImageProcessor:
    """Processador avançado de imagens"""
    
    def __init__(self, flux_api_url: str = None):
        self.flux_api_url = flux_api_url or "https://api.flux-ai.io/v1/generate"
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    def generate_image(self, prompt: str, style: str = "realistic", 
                      size: Tuple[int, int] = (1024, 1024)) -> str:
        """Gera imagem usando IA"""
        try:
            payload = {
                "model": "nano-banana-ai",
                "prompt": f"{prompt}, {style} style",
                "width": size[0],
                "height": size[1],
                "steps": 20,
                "guidance_scale": 7.5
            }
            
            response = requests.post(self.flux_api_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                image_url = result.get("image_url")
                
                if image_url:
                    # Baixa a imagem
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"generated_images/image_{timestamp}.png"
                        
                        os.makedirs("generated_images", exist_ok=True)
                        
                        with open(filename, 'wb') as f:
                            f.write(img_response.content)
                        
                        return filename
            
        except Exception as e:
            print(f"Erro na geração de imagem: {e}")
            # Fallback: cria imagem placeholder
            return self._create_placeholder_image(prompt, size)
        
        return None
    
    def _create_placeholder_image(self, prompt: str, size: Tuple[int, int]) -> str:
        """Cria imagem placeholder quando a geração falha"""
        from PIL import Image, ImageDraw, ImageFont
        
        # Cria imagem com cor baseada no hash do prompt
        hash_color = hash(prompt) % 16777215  # Cor baseada no hash
        color = f"#{hash_color:06x}"
        
        img = Image.new('RGB', size, color=color)
        draw = ImageDraw.Draw(img)
        
        # Adiciona texto
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        text = f"Generated for:\n{prompt[:50]}..."
        draw.text((50, size[1]//2), text, fill="white", font=font)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_images/placeholder_{timestamp}.png"
        
        os.makedirs("generated_images", exist_ok=True)
        img.save(filename)
        
        return filename
    
    def refine_image(self, image_path: str, refinement_prompt: str) -> str:
        """Refina imagem existente"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Imagem não encontrada: {image_path}")
        
        # Carrega imagem
        img = Image.open(image_path)
        
        # Aplica refinamentos baseados no prompt
        refined_img = self._apply_refinements(img, refinement_prompt)
        
        # Salva imagem refinada
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"refined_images/refined_{timestamp}.png"
        
        os.makedirs("refined_images", exist_ok=True)
        refined_img.save(filename)
        
        return filename
    
    def _apply_refinements(self, img: Image.Image, prompt: str) -> Image.Image:
        """Aplica refinamentos baseados no prompt"""
        prompt_lower = prompt.lower()
        
        # Aplica filtros baseados no prompt
        if "blur" in prompt_lower or "suave" in prompt_lower:
            img = img.filter(ImageFilter.GaussianBlur(radius=2))
        
        if "sharp" in prompt_lower or "nítido" in prompt_lower:
            img = img.filter(ImageFilter.SHARPEN)
        
        if "bright" in prompt_lower or "brilho" in prompt_lower:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.3)
        
        if "contrast" in prompt_lower or "contraste" in prompt_lower:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
        
        if "vintage" in prompt_lower or "sépia" in prompt_lower:
            # Aplica efeito sépia
            img = img.convert('RGB')
            pixels = img.load()
            for i in range(img.width):
                for j in range(img.height):
                    r, g, b = pixels[i, j]
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    pixels[i, j] = (min(255, tr), min(255, tg), min(255, tb))
        
        return img
    
    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Analisa imagem e extrai informações"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Imagem não encontrada: {image_path}")
        
        img = Image.open(image_path)
        
        analysis = {
            "filename": os.path.basename(image_path),
            "size": img.size,
            "format": img.format,
            "mode": img.mode,
            "has_transparency": img.mode in ('RGBA', 'LA') or 'transparency' in img.info,
            "colors": self._analyze_colors(img),
            "brightness": self._calculate_brightness(img),
            "objects": self._detect_objects(image_path)  # Simulado
        }
        
        return analysis
    
    def _analyze_colors(self, img: Image.Image) -> Dict[str, Any]:
        """Analisa cores dominantes na imagem"""
        # Reduz imagem para análise mais rápida
        img_small = img.resize((50, 50))
        colors = img_small.getcolors(maxcolors=256*256*256)
        
        if colors:
            # Ordena por frequência
            colors.sort(key=lambda x: x[0], reverse=True)
            dominant_colors = colors[:5]  # Top 5 cores
            
            return {
                "dominant_colors": [{"color": color[1], "frequency": color[0]} 
                                  for color in dominant_colors],
                "total_unique_colors": len(colors)
            }
        
        return {"dominant_colors": [], "total_unique_colors": 0}
    
    def _calculate_brightness(self, img: Image.Image) -> float:
        """Calcula brilho médio da imagem"""
        # Converte para escala de cinza
        grayscale = img.convert('L')
        
        # Calcula média dos pixels
        pixels = list(grayscale.getdata())
        brightness = sum(pixels) / len(pixels) / 255.0
        
        return brightness
    
    def _detect_objects(self, image_path: str) -> List[str]:
        """Simula detecção de objetos (requer integração com modelo de visão)"""
        # Em uma implementação real, usaria um modelo como YOLO ou similar
        # Por enquanto, retorna objetos simulados baseados no nome do arquivo
        filename = os.path.basename(image_path).lower()
        
        detected_objects = []
        
        if "person" in filename or "people" in filename:
            detected_objects.append("person")
        if "car" in filename or "vehicle" in filename:
            detected_objects.append("vehicle")
        if "building" in filename or "house" in filename:
            detected_objects.append("building")
        if "nature" in filename or "tree" in filename:
            detected_objects.append("nature")
        
        return detected_objects if detected_objects else ["unknown_objects"]

class AudioProcessor:
    """Processador avançado de áudio"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self._configure_tts()
    
    def _configure_tts(self):
        """Configura o engine de TTS"""
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)
        
        # Tenta configurar voz em português
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if 'portuguese' in voice.name.lower() or 'brasil' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
    
    def transcribe_audio(self, audio_path: str, language: str = 'pt-BR') -> Dict[str, Any]:
        """Transcreve áudio para texto"""
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
            
            # Tenta diferentes engines de reconhecimento
            transcriptions = {}
            
            # Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio, language=language)
                transcriptions['google'] = {
                    'text': text,
                    'confidence': 0.8  # Estimativa
                }
            except sr.UnknownValueError:
                transcriptions['google'] = {'error': 'Não foi possível entender o áudio'}
            except sr.RequestError as e:
                transcriptions['google'] = {'error': f'Erro no serviço: {e}'}
            
            # Whisper (se disponível)
            whisper_result = self._transcribe_with_whisper(audio_path)
            if whisper_result:
                transcriptions['whisper'] = whisper_result
            
            return {
                'file': os.path.basename(audio_path),
                'language': language,
                'transcriptions': transcriptions,
                'best_transcription': self._select_best_transcription(transcriptions)
            }
            
        except Exception as e:
            return {'error': f'Erro na transcrição: {e}'}
    
    def _transcribe_with_whisper(self, audio_path: str) -> Optional[Dict[str, Any]]:
        """Transcreve usando Whisper.cpp (se disponível)"""
        try:
            # Verifica se whisper está disponível
            whisper_path = self._find_whisper_executable()
            if not whisper_path:
                return None
            
            # Executa whisper
            result = subprocess.run([
                whisper_path,
                '-f', audio_path,
                '-l', 'pt',
                '--output-json'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Parse do resultado JSON
                output = result.stdout
                if output:
                    whisper_data = json.loads(output)
                    return {
                        'text': whisper_data.get('text', ''),
                        'confidence': whisper_data.get('confidence', 0.9),
                        'segments': whisper_data.get('segments', [])
                    }
            
        except Exception as e:
            print(f"Erro no Whisper: {e}")
        
        return None
    
    def _find_whisper_executable(self) -> Optional[str]:
        """Encontra executável do Whisper"""
        possible_paths = [
            './whisper.cpp/main',
            './whisper',
            'whisper',
            '/usr/local/bin/whisper'
        ]
        
        for path in possible_paths:
            if os.path.exists(path) or subprocess.run(['which', path], 
                                                    capture_output=True).returncode == 0:
                return path
        
        return None
    
    def _select_best_transcription(self, transcriptions: Dict[str, Any]) -> Dict[str, Any]:
        """Seleciona a melhor transcrição disponível"""
        # Prioriza Whisper se disponível e com boa confiança
        if 'whisper' in transcriptions and 'text' in transcriptions['whisper']:
            whisper_conf = transcriptions['whisper'].get('confidence', 0)
            if whisper_conf > 0.7:
                return transcriptions['whisper']
        
        # Senão, usa Google
        if 'google' in transcriptions and 'text' in transcriptions['google']:
            return transcriptions['google']
        
        # Fallback
        for engine, result in transcriptions.items():
            if 'text' in result:
                return result
        
        return {'error': 'Nenhuma transcrição bem-sucedida'}
    
    def generate_speech(self, text: str, voice_type: str = 'female', 
                       output_path: str = None) -> str:
        """Gera áudio a partir de texto"""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"generated_audio/speech_{timestamp}.wav"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Configura voz baseada no tipo
        voices = self.tts_engine.getProperty('voices')
        
        if voice_type == 'male':
            # Procura voz masculina
            for voice in voices:
                if 'male' in voice.name.lower() or 'masculin' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        else:
            # Procura voz feminina
            for voice in voices:
                if 'female' in voice.name.lower() or 'feminin' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        
        # Gera áudio
        self.tts_engine.save_to_file(text, output_path)
        self.tts_engine.runAndWait()
        
        return output_path
    
    def analyze_audio(self, audio_path: str) -> Dict[str, Any]:
        """Analisa propriedades do áudio"""
        try:
            # Usa librosa se disponível, senão análise básica
            try:
                import librosa
                y, sr = librosa.load(audio_path)
                
                analysis = {
                    'duration': len(y) / sr,
                    'sample_rate': sr,
                    'channels': 1 if len(y.shape) == 1 else y.shape[0],
                    'rms_energy': float(librosa.feature.rms(y=y).mean()),
                    'spectral_centroid': float(librosa.feature.spectral_centroid(y=y, sr=sr).mean()),
                    'zero_crossing_rate': float(librosa.feature.zero_crossing_rate(y).mean())
                }
                
            except ImportError:
                # Análise básica sem librosa
                analysis = self._basic_audio_analysis(audio_path)
            
            return analysis
            
        except Exception as e:
            return {'error': f'Erro na análise de áudio: {e}'}
    
    def _basic_audio_analysis(self, audio_path: str) -> Dict[str, Any]:
        """Análise básica de áudio sem dependências externas"""
        file_size = os.path.getsize(audio_path)
        
        return {
            'file_size': file_size,
            'format': os.path.splitext(audio_path)[1],
            'estimated_duration': file_size / 16000,  # Estimativa grosseira
            'analysis_type': 'basic'
        }

class VideoProcessor:
    """Processador básico de vídeo"""
    
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv']
    
    def generate_video_from_images(self, image_paths: List[str], 
                                 output_path: str = None, 
                                 duration_per_image: float = 2.0) -> str:
        """Gera vídeo a partir de sequência de imagens"""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"generated_videos/video_{timestamp}.mp4"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            # Usa ffmpeg se disponível
            if self._check_ffmpeg():
                return self._create_video_with_ffmpeg(image_paths, output_path, duration_per_image)
            else:
                # Fallback: cria GIF animado
                return self._create_animated_gif(image_paths, output_path.replace('.mp4', '.gif'))
                
        except Exception as e:
            print(f"Erro na geração de vídeo: {e}")
            return None
    
    def _check_ffmpeg(self) -> bool:
        """Verifica se ffmpeg está disponível"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True)
            return True
        except FileNotFoundError:
            return False
    
    def _create_video_with_ffmpeg(self, image_paths: List[str], 
                                output_path: str, duration: float) -> str:
        """Cria vídeo usando ffmpeg"""
        # Cria arquivo de lista de imagens
        list_file = "temp_image_list.txt"
        with open(list_file, 'w') as f:
            for img_path in image_paths:
                f.write(f"file '{img_path}'\n")
                f.write(f"duration {duration}\n")
        
        try:
            # Executa ffmpeg
            subprocess.run([
                'ffmpeg', '-f', 'concat', '-safe', '0',
                '-i', list_file,
                '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
                '-c:v', 'libx264', '-r', '30', '-pix_fmt', 'yuv420p',
                output_path
            ], check=True)
            
            return output_path
            
        finally:
            # Remove arquivo temporário
            if os.path.exists(list_file):
                os.remove(list_file)
    
    def _create_animated_gif(self, image_paths: List[str], output_path: str) -> str:
        """Cria GIF animado como fallback"""
        images = []
        for img_path in image_paths:
            img = Image.open(img_path)
            # Redimensiona para tamanho padrão
            img = img.resize((800, 600), Image.Resampling.LANCZOS)
            images.append(img)
        
        if images:
            images[0].save(
                output_path,
                save_all=True,
                append_images=images[1:],
                duration=2000,  # 2 segundos por frame
                loop=0
            )
        
        return output_path

class MediaOrchestrator:
    """Orquestrador de todas as funcionalidades de mídia"""
    
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.audio_processor = AudioProcessor()
        self.video_processor = VideoProcessor()
    
    def create_multimedia_content(self, prompt: str, content_type: str = "complete") -> Dict[str, str]:
        """Cria conteúdo multimídia baseado em prompt"""
        results = {}
        
        if content_type in ["complete", "image"]:
            # Gera imagem
            image_path = self.image_processor.generate_image(prompt)
            if image_path:
                results["image"] = image_path
        
        if content_type in ["complete", "audio"]:
            # Gera áudio
            audio_path = self.audio_processor.generate_speech(
                f"Conteúdo gerado para: {prompt}"
            )
            results["audio"] = audio_path
        
        if content_type in ["complete", "video"] and "image" in results:
            # Gera vídeo simples com a imagem
            video_path = self.video_processor.generate_video_from_images([results["image"]])
            if video_path:
                results["video"] = video_path
        
        return results
    
    def analyze_media_file(self, file_path: str) -> Dict[str, Any]:
        """Analisa arquivo de mídia automaticamente"""
        if not os.path.exists(file_path):
            return {"error": "Arquivo não encontrado"}
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in self.image_processor.supported_formats:
            return self.image_processor.analyze_image(file_path)
        elif file_ext in ['.wav', '.mp3', '.m4a', '.flac']:
            return self.audio_processor.analyze_audio(file_path)
        elif file_ext in self.video_processor.supported_formats:
            return {"type": "video", "message": "Análise de vídeo não implementada"}
        else:
            return {"error": f"Formato não suportado: {file_ext}"}

# Exemplo de uso
if __name__ == "__main__":
    orchestrator = MediaOrchestrator()
    
    # Testa geração de conteúdo multimídia
    content = orchestrator.create_multimedia_content(
        "Uma paisagem futurista com inteligência artificial",
        content_type="complete"
    )
    
    print("Conteúdo gerado:")
    for media_type, path in content.items():
        print(f"  {media_type}: {path}")

