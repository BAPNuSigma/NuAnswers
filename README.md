# 💬 NuAnswers - AI Tutoring Bot

NuAnswers is an intelligent tutoring bot developed by Beta Alpha Psi: Nu Sigma Chapter. It provides personalized assistance in accounting, finance, and related subjects while encouraging learning through guided problem-solving rather than direct answers.

## 🌟 Features

### 🎓 Intelligent Tutoring
- Step-by-step guidance through problems
- Encourages critical thinking
- Avoids giving direct answers
- Personalized learning experience
- Supports accounting, finance, and related topics

### 📚 Document Support
- Upload and process various file formats:
  - PDF documents
  - Word documents (DOCX)
  - Text files (TXT)
  - PowerPoint presentations (PPTX)
  - Excel spreadsheets (XLS, XLSX)
  - CSV files
  - Images (PNG, JPG, JPEG) with AI-powered analysis
- Intelligent image analysis for:
  - Screenshots of problems or equations
  - Charts and graphs
  - Handwritten notes
  - Financial statements
  - Business diagrams
- Search within uploaded documents
- Manage and reorder documents
- Context-aware tutoring based on uploaded materials

### 🤖 AI-Powered Features
- Intelligent tutoring with step-by-step guidance
- Image analysis using GPT-4 Vision
- Natural language understanding
- Context-aware responses
- Personalized learning experience

### ⏰ Smart Availability
- Automatically manages access based on in-person tutoring hours
- Encourages in-person tutoring during scheduled sessions
- Available 24/7 outside of tutoring hours

### 📊 Advanced Analytics Dashboard
#### Overview Metrics
- Total registrations and unique students
- Total and average usage time
- Return user analysis and retention rates

#### Time-Based Analytics
- Daily and weekly usage patterns
- Peak usage times heatmap
- Session duration analysis
- Hourly distribution of activity

#### Academic Performance Metrics
- Grade level progression analysis
- Major and course distribution
- Cross-analysis of academic factors
- Professor engagement statistics

#### User Engagement Metrics
- Session frequency patterns
- Time between sessions analysis
- Return user behavior
- User retention statistics

#### Document Analytics
- File type distribution
- Documents per student
- Upload patterns and trends

#### Chat Interaction Analysis
- Message statistics and patterns
- Average message length
- User engagement metrics
- Interaction frequency

#### Enhanced Filtering and Export
- Multi-dimensional data filtering
- Date range selection
- Major and campus filtering
- Export to CSV and Excel formats

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- OpenAI API key (with GPT-4 Vision access)
- Streamlit account (for deployment)

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd NuAnswers
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Create a `.streamlit/secrets.toml` file:
```toml
OPENAI_API_KEY = "your-api-key-here" # Must have GPT-4 Vision access
ADMIN_PASSWORD = "your-admin-password-here"
```

### Running Locally

```bash
streamlit run streamlit_app.py
```

### Deployment on Render

1. Create a new Web Service on Render
2. Connect your repository
3. Add environment variables:
   - `OPENAI_API_KEY`
   - `ADMIN_PASSWORD`
4. Configure HTTPS:
   - Render automatically provides SSL/TLS certificates
   - Wait a few minutes after deployment for the certificate to be issued
   - Access the app using `https://` instead of `http://`
   - If you see a certificate warning, wait a few minutes and refresh
5. Deploy the service

## 🔐 Configuration

### File Upload Limits
- Maximum file size: 200MB
- Supported formats: 
  - Documents: PDF, DOCX, TXT, PPTX, CSV, XLS, XLSX
  - Images: PNG, JPG, JPEG
  - Image analysis is automatic for supported image formats

### Tutoring Hours
Modify the `TUTORING_HOURS` dictionary in `streamlit_app.py`:
```python
TUTORING_HOURS = {
    "Monday": [("10:30", "12:30")],    # 10:30 AM - 12:30 PM
    "Tuesday": [("17:00", "19:00")],   # 5:00 PM - 7:00 PM
    "Wednesday": [("12:00", "14:00")], # 12:00 PM - 2:00 PM
    "Thursday": [("10:30", "12:30")],  # 10:30 AM - 12:30 PM
    "Friday": [("13:00", "15:00")],    # 1:00 PM - 3:00 PM
}
```

## 👥 User Types

### Students
- Complete registration form
- Upload course materials and images
- Get AI analysis of uploaded images
- Interact with the tutoring bot
- Search and manage uploaded documents

### Administrators
- Access comprehensive usage statistics
- Monitor real-time engagement metrics
- Track academic performance patterns
- Analyze user behavior and retention
- View document and image upload statistics
- Export detailed analytics reports
- Filter and customize data views
- Monitor chat interaction patterns

## 📝 Registration Data
The system collects and analyzes:
- Full Name
- Student ID (must be exactly 7 digits)
- Email (must use @student.fdu.edu or @fdu.edu domain)
- Grade Level
- Campus
- Major
- Course Information
- Usage Statistics
- Session Patterns
- Document Upload History
- Image Analysis Data
- Chat Interaction Data

## 🔒 Security Features
- Password-protected admin access
- Secure API key management
- User data encryption
- Session management
- HTTPS encryption
- Strict Transport Security (HSTS)
- Secure cookie handling
- Input validation and sanitization:
  - Student ID validation (7 digits)
  - Email domain validation (@student.fdu.edu or @fdu.edu)
  - Required field checks
- Secure image processing

## 🤝 Contributing
We welcome contributions! Please feel free to submit pull requests.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
- Beta Alpha Psi: Nu Sigma Chapter
- OpenAI for GPT API and GPT-4 Vision
- Streamlit for the web framework

## 🔐 Troubleshooting

### Image Upload Issues
If you experience issues with image uploads:
1. Ensure the image is in a supported format (PNG, JPG, JPEG)
2. Check that the file size is within limits
3. Verify your internet connection is stable
4. Make sure your OpenAI API key has GPT-4 Vision access
5. Try converting the image to a different supported format

### SSL/HTTPS Issues
If you see a certificate warning:
1. Make sure you're using `https://` in the URL
2. Wait a few minutes after deployment for the certificate to be issued
3. Clear your browser cache and refresh
4. If the issue persists, contact Render support

### Security Best Practices
1. Always use HTTPS when accessing the application
2. Keep your API keys secure and never share them
3. Regularly update your admin password
4. Monitor the application logs for any suspicious activity
