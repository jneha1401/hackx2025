# SwasthyaLink Frontend

React frontend for SwasthyaLink - A multilingual healthcare platform.

## Features

- **Multi-language Support**: English, Hindi, Marathi, Kannada
- **Role-based Access**: Patient and Doctor dashboards
- **Video Calling**: Integrated ZegoCloud video conferencing
- **Responsive Design**: Modern UI with animations
- **Healthcare Focused**: Consult, Records, and Communication features

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or pnpm

### Installation

```bash
# Install dependencies
npm install
# or
pnpm install

# Start development server
npm run dev
# or
pnpm run dev
```

The application will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
# or
pnpm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx          # Main application component
│   ├── main.jsx         # React entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
└── vite.config.js       # Vite configuration
```

## Technologies Used

- **React 18** - Frontend framework
- **Vite** - Build tool and dev server
- **ZegoCloud** - Video calling integration
- **Font Awesome** - Icons
- **Google Fonts** - Typography (Nunito)

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
