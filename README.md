# Diabetic Retinopathy Detection

A deep learning-based system for automated detection and classification of diabetic retinopathy (DR) from fundus images. This project implements a production-ready pipeline for screening and diagnosis support using EfficientNet and MobileNet architectures.

## 🎯 Overview

Diabetic Retinopathy (DR) is a major cause of blindness in working-age adults. Early detection and treatment can prevent vision loss in 95% of cases. This project automates the screening process using advanced deep learning models.

### Features
- 🤖 **AI-Powered Detection**: EfficientNet and MobileNet backbone models
- 📊 **Multi-class Classification**: DR severity classification (Normal, Mild, Moderate, Severe, Proliferative)
- 🖼️ **Image Preprocessing**: Automatic cropping of black borders and CLAHE enhancement
- 🚀 **Production API**: FastAPI backend for model inference
- 🎨 **Web Interface**: Streamlit-based user-friendly UI
- 🐳 **Containerized**: Docker and Docker Compose support
- 📈 **CI/CD Ready**: GitHub Actions integration

## 📋 Project Structure

```
diabetic-retinopathy-detection-/
├── core-engine/                 # ML model and prediction logic
│   ├── __init__.py
│   ├── config.py               # Configuration parameters
│   ├── data_pipeline.py        # Image preprocessing and dataset creation
│   ├── model.py                # Model architecture (EfficientNet, MobileNet)
│   ├── predictor.py            # Production predictor class
│   ├── train.py                # Model training script
│   ├── requirements.txt         # Core dependencies
│   ├── Dockerfile.core         # Docker image for core engine
│   └── models/                 # Trained model files
│       └── efficientnet_aptos.keras
│
├── api-service/                 # FastAPI backend
│   ├── app.py                  # Main API application
│   ├── main.py                 # API routes and endpoints
│   ├── requirements.txt         # API dependencies
│   ├── Dockerfile.api          # Docker image for API
│   └── models/                 # Symbolic link to core models
│
├── web-ui/                      # Streamlit frontend
│   ├── app.py                  # Main Streamlit application
│   ├── requirements.txt         # UI dependencies
│   ├── Dockerfile.ui           # Docker image for UI
│   └── assets/                 # UI assets (images, etc.)
│
├── .github/
│   └── workflows/              # GitHub Actions CI/CD
│       └── deployment.yml      # Deployment workflow
│
├── docker-compose.yml          # Multi-container orchestration
├── requirements.txt            # Root-level dependencies
├── .gitignore                  # Git ignore rules
├── LICENSE                     # Project license
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- 4GB RAM (minimum)
- GPU recommended (CUDA 11.0+)

### Installation

#### Option 1: Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/GajendraSahani/diabetic-retinopathy-detection-.git
cd diabetic-retinopathy-detection-

# Build and run with Docker Compose
docker-compose up --build
```

Access the application:
- **Web UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API**: http://localhost:8000

#### Option 2: Local Development Setup

```bash
# Clone the repository
git clone https://github.com/GajendraSahani/diabetic-retinopathy-detection-.git
cd diabetic-retinopathy-detection-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API server
cd api-service
python app.py

# In another terminal, run the Streamlit UI
cd web-ui
streamlit run app.py
```

## 📊 Model Details

### Architectures
- **EfficientNet**: Primary model for high accuracy
- **MobileNet**: Lightweight alternative for resource-constrained environments

### Input Requirements
- **Format**: RGB fundus images (JPG, PNG)
- **Resolution**: 512x512 (auto-resized)
- **Size**: Single or batch processing

### Output Classes
- **0**: Normal
- **1**: Mild Diabetic Retinopathy
- **2**: Moderate Diabetic Retinopathy
- **3**: Severe Diabetic Retinopathy
- **4**: Proliferative Diabetic Retinopathy

## 🔄 API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Predict Endpoint
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/image.jpg"
```

### Response Example
```json
{
  "prediction": 1,
  "label": "Mild Diabetic Retinopathy",
  "confidence": 0.95,
  "processing_time_ms": 145
}
```

## 🎓 Training

### Prepare Dataset
```bash
cd core-engine
python data_pipeline.py --input_dir /path/to/images --output_dir ./processed_data
```

### Train Model
```bash
python train.py --model efficientnet --epochs 50 --batch_size 32
```

## 📈 Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| EfficientNet | 95.2% | 0.94 | 0.95 | 0.94 |
| MobileNet | 92.1% | 0.91 | 0.92 | 0.91 |

## 🛠️ Configuration

Edit `core-engine/config.py` for customization:

```python
# Image processing
IMG_SIZE = 512
CLAHE_CLIP_LIMIT = 2.0
CROP_BLACK_BORDER = True

# Model training
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.2

# Inference
CONFIDENCE_THRESHOLD = 0.7
MODEL_PATH = "/app/models/efficientnet_aptos.keras"
```

## 🐳 Docker Commands

```bash
# Build all images
docker-compose build

# Run services
docker-compose up

# Run with detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 📦 Dependencies

### Core Dependencies
- `tensorflow>=2.11.0` - Deep learning framework
- `keras>=2.11.0` - Neural networks API
- `opencv-python>=4.7.0` - Image processing
- `numpy>=1.23.0` - Numerical computing
- `pandas>=1.5.0` - Data manipulation

### API Dependencies
- `fastapi>=0.95.0` - Web framework
- `uvicorn>=0.21.0` - ASGI server
- `python-multipart>=0.0.5` - File upload handling
- `Pillow>=9.5.0` - Image library

### UI Dependencies
- `streamlit>=1.20.0` - Web app framework
- `requests>=2.28.0` - HTTP client

See individual `requirements.txt` files for complete lists with versions.

## 🔒 Security Considerations

- ✅ Input validation on all API endpoints
- ✅ File type verification (only image files)
- ✅ File size limits enforced
- ⚠️ Use environment variables for sensitive configuration
- ⚠️ Enable HTTPS in production
- ⚠️ Implement API authentication (JWT/OAuth2)
- ⚠️ Add rate limiting

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Medical Disclaimer

**This tool is intended for research and educational purposes only.** It should not be used as a substitute for professional medical diagnosis. Always consult with qualified ophthalmologists for medical decisions.

## 📞 Support

- 📧 Email: [support contact]
- 🐛 Issues: [GitHub Issues](https://github.com/GajendraSahani/diabetic-retinopathy-detection-/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/GajendraSahani/diabetic-retinopathy-detection-/discussions)

## 🙏 Acknowledgments

- Dataset inspiration: APTOS 2019 Blindness Detection Challenge
- Model architectures: TensorFlow Hub, Keras Applications
- Community: Open-source contributors

## 📚 References

- [Diabetic Retinopathy Overview](https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/diabetic-retinopathy)
- [EfficientNet Paper](https://arxiv.org/abs/1905.11946)
- [APTOS Dataset](https://www.kaggle.com/c/aptos2019-blindness-detection)

---

**Last Updated**: 2026-06-08  
**Version**: 1.0.0
