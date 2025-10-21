async function setupWebcam(videoId) {
  const video = document.getElementById(videoId);
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } },
      audio: false
    });
    video.srcObject = stream;
  } catch (e) {
    console.error('Webcam error', e);
    alert('Não foi possível acessar a câmera. Verifique as permissões.');
  }
}

function captureFace(videoId, canvasId) {
  const video = document.getElementById(videoId);
  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext('2d');
  const width = video.videoWidth || 640;
  const height = video.videoHeight || 480;
  canvas.width = width;
  canvas.height = height;
  ctx.drawImage(video, 0, 0, width, height);
  return canvas.toDataURL('image/jpeg', 0.98);
}
