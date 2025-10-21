# Sprint 04 - IOT

Aplicação com autenticação por senha e login por reconhecimento facial.

## Requisitos
- Python 3.10+ (recomendado)
- Windows: instalar Microsoft C++ Build Tools e Visual Studio Redistributables para compilar dependências nativas se necessário
- Webcam no navegador (Chrome/Edge)

## Instalação
```bash
python3 -m venv .venv
pip install -r requirements.txt
```

Se tiver problemas com `tensorflow` no Windows, você pode removê-lo do `requirements.txt` e deixar o DeepFace usar outro backend (menos preciso, mas mais leve), ou instalar uma versão compatível com sua GPU/CPU.

## Executar
```bash
set FLASK_APP=run.py
set FLASK_ENV=development
python run.py
```
Acesse `http://localhost:5000`.

## Fluxo
- Registro: usuário cria conta, opcionalmente captura biometria facial.
- Login: via senha ou via reconhecimento facial.
- Dashboard: registrar eventos de aposta e ver total gasto.

## Observações de segurança
- Este projeto é demonstrativo: armazena embeddings faciais no banco (JSON). Em produção, use criptografia em repouso, política de consentimento e LGPD.
- Ajuste o threshold de similaridade em `app/face_utils.py` conforme testes reais.