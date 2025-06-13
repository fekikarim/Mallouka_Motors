<div align="center">

# 🚗 Mallouka Motors

### *Professional Motor Management System*

<img width="180" src="src/assets/logo/mallouka_motors_logo.svg" alt="Mallouka Motors Logo">
<br>
<img width="500" src="src/assets/demo/demo_mallouka_motors.gif" alt="Mallouka Motors Demo">
<br><br>

[![Python](https://skillicons.dev/icons?i=python)](https://python.org)
<a href="https://flet.dev">
 <img src="https://flet.dev/img/logo.svg" alt="Flet Logo" width="50">
</a>
[![SQLite](https://skillicons.dev/icons?i=sqlite)](https://sqlite.org)

[![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)](LICENSE)

---

</div>

## 📋 About the Project

**Mallouka Motors** is a comprehensive, user-friendly desktop and mobile application engineered to revolutionize motor dealership operations. Built with modern Python technologies and the powerful Flet framework, this solution delivers seamless management of inventory, clients, billing, and business analytics.

> 🎯 **Mission**: Streamline automotive business operations through intelligent automation and intuitive design.

This project represents a successful freelance collaboration between **Karim Feki** and **Mallouka Motors**, delivering exceptional value and operational efficiency that has exceeded client expectations.

---

## 🎬 Application Demo

<div align="center">

### 🌙 Dark Mode Interface
<img width="600" src="src/assets/demo/demo_dash_dark.png" alt="Dark Mode Dashboard">

<br>

### ☀️ Light Mode Interface
<img width="600" src="src/assets/demo/demo_dash_light.png" alt="Light Mode Dashboard">

</div>

## ✨ Key Features

<div align="center">

| Feature | Description | Status |
|---------|-------------|--------|
| 📊 **Analytics Dashboard** | Real-time KPIs, revenue tracking, and business insights | ✅ Complete |
| 💰 **Smart Billing System** | Automated invoice generation with PDF export | ✅ Complete |
| 🚗 **Motor Inventory** | Complete CRUD operations for motor management | ✅ Complete |
| 👥 **Client Management** | Comprehensive customer relationship management | ✅ Complete |
| 🎨 **Theme Customization** | Light/Dark mode with modern UI/UX | ✅ Complete |

</div>

### 📊 Dashboard & Analytics
- **Real-time Metrics**: Total revenue, client count, motors sold, and inventory status
- **Interactive Charts**: Visual representation of sales trends and inventory distribution
- **Performance Indicators**: Key business metrics at a glance
- **Data Visualization**: Modern charts and graphs for better insights

### 💰 Billing Management
- **📄 Invoice Generation**: Professional PDF invoices with company branding
- **🔄 Multi-Motor Billing**: Support for multiple motors per invoice
- **💳 Payment Tracking**: Monitor payment status and methods
- **📋 Billing History**: Complete transaction records with search functionality

### 🚗 Motors Management
- **➕ Add New Motors**: Comprehensive motor registration with all specifications
- **✏️ Edit & Update**: Real-time inventory updates with validation
- **🔍 Advanced Search**: Filter by brand, model, year, status, and price range
- **📈 Status Tracking**: Available, sold, reserved status management
- **💾 Data Integrity**: Robust validation and error handling

### 👥 Clients Management
- **📝 Client Registration**: Complete customer profile management
- **📞 Contact Management**: Phone numbers, addresses, and tax information
- **🔄 Real-time Updates**: Instant synchronization across all modules
- **🔍 Quick Search**: Fast client lookup and filtering capabilities

### ⚙️ Settings & Customization
- **🎨 Theme Switcher**: Seamless light/dark mode transitions
- **ℹ️ About Section**: Company information and application details
- **🔧 Configuration**: Customizable application settings

---

## 🛠️ Technology Stack

<div align="center">

### Core Technologies
[![Python](https://skillicons.dev/icons?i=python)](https://python.org)
<a href="https://flet.dev">
 <img src="https://flet.dev/img/logo.svg" alt="Flet Logo" width="50">
</a>
[![SQLite](https://skillicons.dev/icons?i=sqlite)](https://sqlite.org)

### Key Libraries & Tools
[![ReportLab](https://img.shields.io/badge/ReportLab-PDF_Generation-red?style=for-the-badge)](https://reportlab.com)
[![SQLite Utils](https://img.shields.io/badge/SQLite_Utils-Database_Management-lightblue?style=for-the-badge)](https://sqlite-utils.datasette.io)
[![Python Dotenv](https://img.shields.io/badge/Python_Dotenv-Environment-green?style=for-the-badge)](https://pypi.org/project/python-dotenv)

</div>

### 🏗️ Architecture Overview

```
📁 Mallouka Motors
├── 🎯 Frontend (Flet Framework)
│   ├── 📊 Dashboard Module
│   ├── 🚗 Motors Management
│   ├── 👥 Clients Management
│   ├── 💰 Billing System
│   └── ⚙️ Settings & Themes
├── 🗄️ Backend (Python + SQLite)
│   ├── 📋 Database Models
│   ├── 🔄 CRUD Operations
│   └── 📄 PDF Generation
└── 🎨 Assets & Resources
    ├── 🖼️ Demo Images/GIFs
    ├── 🎨 Icons & Logos
    └── 📝 Documentation
```

### 💡 Technical Highlights

- **🚀 Cross-Platform**: Desktop and mobile compatibility through Flet framework
- **⚡ Real-time Updates**: Instant data synchronization across all modules
- **🔒 Data Integrity**: Robust validation and error handling mechanisms
- **🎨 Modern UI/UX**: Material Design principles with custom theming
- **📱 Responsive Design**: Adaptive layouts for different screen sizes
- **🔄 Efficient Database**: Optimized SQLite queries with proper indexing

---

## 🚀 Getting Started

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Git** for version control
- **Virtual environment** (recommended)

### ⚡ Quick Installation

```bash
# Clone the repository
git clone https://github.com/fekikarim/Mallouka_Motors.git
cd Mallouka_Motors

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

### 🔧 Development Setup

```bash
# Install development dependencies
pip install -e .

# Initialize database (if needed)
python src/db.py

# Run in development mode
flet run src/main.py
```

---

## 🤝 Contributing

<div align="center">

**We welcome contributions from the community!** 🎉

[![Contributors](https://img.shields.io/badge/Contributors-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)
[![Issues](https://img.shields.io/badge/Issues-Open-blue?style=for-the-badge)](https://github.com/fekikarim/Mallouka_Motors/issues)
[![Pull Requests](https://img.shields.io/badge/PRs-Welcome-orange?style=for-the-badge)](https://github.com/fekikarim/Mallouka_Motors/pulls)

</div>

### 🛠️ How to Contribute

1. **🍴 Fork** the repository
2. **🌿 Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **💻 Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **📤 Push** to the branch (`git push origin feature/AmazingFeature`)
5. **🔄 Open** a Pull Request

### 🐛 Bug Reports & Feature Requests

- **🐛 Found a bug?** [Open an issue](https://github.com/fekikarim/Mallouka_Motors/issues/new?template=bug_report.md)
- **💡 Have an idea?** [Request a feature](https://github.com/fekikarim/Mallouka_Motors/issues/new?template=feature_request.md)

### 📝 Development Guidelines

- Follow **PEP 8** coding standards
- Write **clear commit messages**
- Add **tests** for new features
- Update **documentation** as needed

---

## 🏆 Acknowledgments

<div align="center">

### 🤝 Special Thanks

<table>
<tr>
<td align="center" width="50%">
<br>
<strong>🏢 Mallouka Motors</strong>
<br>
<em>For trusting us with their digital transformation journey and providing the opportunity to create this comprehensive business solution that revolutionizes motor dealership operations.</em>
<br>
</td>
<td align="center" width="50%">
<br>
<strong>🎯 Project Impact</strong>
<br>
<em>Delivered exceptional value and operational efficiency that exceeded client expectations, establishing a new standard for automotive business management systems.</em>
<br>
</td>
</tr>
</table>

</div>

---

### 👨‍💻 Development Team

<div align="center">

<table>
<tr>
<td align="center" width="100%">
<br>
<img width="150" height="150" src="https://github.com/fekikarim.png" alt="Karim Feki" style="border-radius: 50%;">
<br><br>
<img src="https://img.shields.io/badge/Lead_Developer-Karim_Feki-blue?style=for-the-badge&logo=github&logoColor=white" alt="Developer Badge">
<br><br>
<strong>🚀 Project Architect & Full-Stack Developer</strong>
<br><br>
</td>
</tr>
</table>

<table>
<tr>
<td align="center" width="25%">
<br>
<strong>🎯 Full-Stack Development</strong>
<br>
<em>End-to-end application architecture, from database design to user interface implementation</em>
<br>
</td>
<td align="center" width="25%">
<br>
<strong>🎨 UI/UX Design</strong>
<br>
<em>Modern interface design with focus on user experience and accessibility</em>
<br>
</td>
<td align="center" width="25%">
<br>
<strong>📊 Database Architecture</strong>
<br>
<em>Optimized SQLite database design with efficient queries and data integrity</em>
<br>
</td>
<td align="center" width="25%">
<br>
<strong>🔧 System Optimization</strong>
<br>
<em>Performance tuning and code optimization for maximum efficiency</em>
<br>
</td>
</tr>
</table>

</div>

---

## 📄 License

<div align="center">

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## 📞 Contact & Support

<div align="center">

### 🤝 Let's Connect!

<table>
<tr>
<td align="center" width="33.33%">
<a href="mailto:feki.karim28@gmail.com">
<img src="https://skillicons.dev/icons?i=gmail" alt="Email">
</a>
<br>
<strong>📧 Direct Email</strong>
<br>
<em>For project inquiries and collaboration opportunities</em>
</td>
<td align="center" width="33.33%">
<a href="https://www.linkedin.com/in/karimfeki/">
<img src="https://skillicons.dev/icons?i=linkedin" alt="LinkedIn">
</a>
<br>
<strong>💼 Professional Network</strong>
<br>
<em>Connect for business opportunities and networking</em>
</td>
<td align="center" width="33.33%">
<a href="https://github.com/fekikarim">
<img src="https://skillicons.dev/icons?i=github" alt="GitHub">
</a>
<br>
<strong>💻 Open Source</strong>
<br>
<em>Explore projects and contribute to development</em>
</td>
</tr>
</table>

</div>

---

### 💼 Professional Services

<div align="center">

<table>
<tr>
<td align="center" width="50%">
<br>
<strong>🚀 Custom Software Development</strong>
<br>
<em>Tailored solutions built with modern technologies to meet your specific business requirements</em>
<br><br>
<br>
<strong>📱 Cross-Platform Applications</strong>
<br>
<em>Desktop and mobile applications that work seamlessly across all platforms</em>
<br>
</td>
<td align="center" width="50%">
<br>
<strong>🎨 UI/UX Design</strong>
<br>
<em>Modern, intuitive interfaces designed with user experience and accessibility in mind</em>
<br><br>
<br>
<strong>🔧 System Integration</strong>
<br>
<em>Seamless integration of existing systems with new technologies and platforms</em>
<br>
</td>
</tr>
<tr>
<td align="center" colspan="2">
<br>
<strong>📊 Business Analytics Solutions</strong>
<br>
<em>Data-driven insights and reporting systems to optimize your business operations and decision-making</em>
<br>
</td>
</tr>
</table>

<br>

### 🎯 Why Choose Our Services?

<table>
<tr>
<td align="center" width="25%">
<br>
<strong>✨ Quality Assured</strong>
<br>
<em>High-quality code and thorough testing</em>
<br>
</td>
<td align="center" width="25%">
<br>
<strong>🛠️ Ongoing Support</strong>
<br>
<em>Continuous maintenance and updates</em>
<br>
</td>
<td align="center" width="25%">
<br>
<strong>⏰ Timely Delivery</strong>
<br>
<em>Projects delivered on schedule</em>
<br>
</td>
<td align="center" width="25%">
<br>
<strong>💬 Clear Communication</strong>
<br>
<em>Regular updates and transparency</em>
<br>
</td>
</tr>
</table>

</div>

---

<div align="center">

**⭐ If you found this project helpful, please consider giving it a star!**

[![Stars](https://img.shields.io/github/stars/fekikarim/Mallouka_Motors?style=social)](https://github.com/fekikarim/Mallouka_Motors/stargazers)
[![Forks](https://img.shields.io/github/forks/fekikarim/Mallouka_Motors?style=social)](https://github.com/fekikarim/Mallouka_Motors/network/members)

</div>

</div>

---

<div align="center">

**Made with ❤️ by [Karim Feki](https://github.com/fekikarim)**

*Transforming business operations through innovative technology solutions*

</div>