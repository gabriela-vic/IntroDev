## The Science of Fashion
### About
An interactive web experience exploring the intersection between scientific principles and the fashion industry.
### Key Objectives
* Educate users on the textile production cycle.
* Raise awareness about the environmental impact of the fashion industry.
* Demystify the intricacies of the many different fibers and materials used in garments.
* Explore the social significance of fashion as a means of expression and political activism. 
### Main Features

#### Interactive Microscope
Users can explore a detailed microscope view of different textile fibers, organized by category (Natural and Synthetic). Each fiber displays:
* Name and origin information
* Detailed descriptions of fiber properties
* Navigation between fibers in the same category
* Ability to favorite fibers for quick access later

#### User Accounts & Authentication
* Create an account with username, email, and password
* Login/logout functionality with secure cookie-based sessions
* User profiles with customizable bio information
* Account management (edit profile or delete account)

#### Favorite Items
* Save favorite fibers and blog posts to a personal collection
* Access favorites from the user profile dashboard
* Quick navigation from favorites directly to detail pages

#### Blog System
* Read educational articles about fashion and textiles
* Navigate between posts with previous/next buttons
* Post comments on articles (logged-in users only)
* Search and favorite blog posts
* Clean, card-based layout for infinite scroll-like experience

#### Search Functionality
* Real-time search across fiber names, categories, and origins
* Case-insensitive matching (search "alg" finds "Algodão")
* Dropdown results with quick navigation to fiber details
* Smooth debounced search with minimal server requests

### Future Implementations

#### Educational Lab Features
* **Cadeia Textil (Textile Chain)**: Interactive visualization of the entire textile production process from raw material to finished garment
* **Timeline**: Historical evolution of textiles and their impact on society and the environment
* **Sustainability Calculator**: Tool to help users calculate the environmental impact of different fabrics and production methods

#### Additional Features
* Advanced filtering and sorting in fiber explorer
* User-generated content moderation system
* Statistics and analytics about fashion sustainability
* Integration with external databases for real-time material sourcing information

### Technology & Development

#### AI Assistance
This project was developed with a combination of independent work and AI assistance:

* **Backend Development**: Primarily developed independently using materials and resources from [webdev2025.lol](https://webdev2025.lol/), with foundational knowledge in FastAPI, SQLModel, and database design.
* **Frontend-Backend Integration**: AI assistance was crucial for debugging and implementing HTMX button integrations and search functionality. This helped bridge the gap between frontend interactions and backend API responses.
* **Frontend Styling**: CSS and visual design were developed collaboratively with AI, using iterative feedback and suggestions to refine the UI/UX across different pages and features.

#### Project Stack
* **Backend**: FastAPI, SQLModel, SQLite
* **Frontend**: HTML, Jinja2 Templates, CSS
* **Interactivity**: HTMX for dynamic page updates without full page reloads
* **Design**: Custom CSS with responsive breakpoints for mobile, tablet, and desktop

### Getting Started & Usage

#### Prerequisites
* Python 3.8 or higher
* pip (Python package manager)

#### Installation Steps

**Step 1:** Clone this repository to your local machine.
```bash
git clone <repository-url>
cd IntroDev/Projeto-01
```

**Step 2:** Create a virtual environment (recommended).
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Step 3:** Install project dependencies.
```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes:
* **FastAPI** - Web framework for building the backend API
* **Uvicorn** - ASGI server to run the application
* **SQLModel** - ORM for database management
* **Jinja2** - Template engine for HTML rendering
* **python-multipart** - For handling form submissions

**Step 4:** Populate the database with sample data.
```bash
python3 seed.py
```

The `seed.py` script initializes the database with:
* 50+ textile fibers (natural and synthetic) with detailed information
* Microscope observations for each fiber
* Sample blog posts about fashion and sustainability
* User accounts for testing (you can also create your own)

This creates a `database.db` file that stores all application data.

**Step 5:** Run the development server.
```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`. The `--reload` flag automatically restarts the server when you make code changes.

**Step 6:** Open your browser and navigate to `http://localhost:8000` to start exploring!

#### Testing the Application

* **Create an account**: Click the account icon in the top-right, select "Cadastrar" (Register)
* **Login**: Use your credentials to log in
* **Explore fibers**: Navigate to "Laboratório" → "Microscópio" to view fibers
* **Search**: Use the search bar to find fibers by name, type, or origin
* **Favorite items**: Mark fibers and blog posts as favorites (when logged in)
* **Read blog**: Check out the "Blog" section for educational articles
* **View profile**: Access your profile to see favorites and edit your information

### Support & Feedback
If you have questions, suggestions, or encounter any issues, feel free to open an Issue in this repository or contact the maintener.
### Author & Maintener
Developed and maintained by Gabriela Victor.
You can contact me at gabevictor333@gmail.com
