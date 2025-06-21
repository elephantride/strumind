# StruMind - Structural Engineering Analysis Platform

## Overview

StruMind is a full-stack web application for structural engineering analysis and design. It provides a modern interface for creating 3D structural models, performing engineering analysis, and visualizing results. The application is built with React, Express, and PostgreSQL, featuring a comprehensive structural engineering workflow from model creation to code compliance checking.

## System Architecture

The application follows a **monorepo full-stack architecture** with clear separation between client and server components:

### Architecture Pattern
- **Frontend**: React SPA with TypeScript
- **Backend**: Express.js REST API server
- **Database**: PostgreSQL with Drizzle ORM
- **Development**: Unified development experience via Vite
- **Deployment**: Static frontend with Node.js backend on Replit

### Project Structure
```
├── client/           # React frontend application
├── server/           # Express.js backend API
├── shared/           # Shared types and schemas
├── migrations/       # Database migration files
└── config files      # Build and development configuration
```

## Key Components

### Frontend Architecture (React + TypeScript)
- **UI Framework**: Radix UI primitives with shadcn/ui components
- **Styling**: Tailwind CSS with design system
- **State Management**: React Query for server state, local state for UI
- **Routing**: Wouter for client-side routing
- **Build Tool**: Vite for development and production builds

### Backend Architecture (Express.js)
- **API Pattern**: RESTful API with `/api` prefix routing
- **Database Layer**: Drizzle ORM with PostgreSQL
- **Storage Abstraction**: Interface-based storage layer (currently in-memory, ready for database)
- **Development**: Hot reload with tsx, production build with esbuild

### Database Schema (PostgreSQL + Drizzle)
The database supports comprehensive structural engineering workflows:
- **Users**: Authentication and user management
- **Projects**: Project organization and metadata
- **Nodes**: 3D coordinate system for structural nodes
- **Elements**: Structural elements (beams, columns) with properties
- **Load Cases**: Different loading scenarios
- **Analysis Results**: Computed engineering results

### UI Component System
- **Design System**: Consistent theming with CSS variables
- **Component Library**: Comprehensive set of reusable components
- **Accessibility**: Built on Radix UI primitives for accessibility compliance
- **Responsive Design**: Mobile-first approach with Tailwind breakpoints

## Data Flow

### Client-Server Communication
1. **API Requests**: React Query manages all server communication
2. **Error Handling**: Centralized error handling with toast notifications
3. **Loading States**: Built-in loading and error states via React Query
4. **Caching**: Intelligent caching strategy for performance

### Application Workflow
1. **Model Building**: Users create 3D structural models with nodes and elements
2. **Load Definition**: Define load cases and boundary conditions
3. **Analysis**: Run structural analysis calculations
4. **Design Verification**: Check against engineering codes (AISC, etc.)
5. **Visualization**: 3D viewing and results presentation

## External Dependencies

### Core Framework Dependencies
- **React 18**: Frontend framework with modern hooks
- **Express**: Backend web framework
- **Drizzle ORM**: Type-safe database ORM
- **Neon Database**: Serverless PostgreSQL provider

### UI and Styling
- **Radix UI**: Headless component primitives
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide Icons**: Consistent icon system
- **Class Variance Authority**: Type-safe variant management

### Development Tools
- **TypeScript**: Type safety across the stack
- **Vite**: Fast development and build tool
- **ESBuild**: Production backend bundling
- **Drizzle Kit**: Database migration management

## Deployment Strategy

### Replit Deployment Configuration
- **Environment**: Node.js 20 with PostgreSQL 16
- **Build Process**: 
  1. Frontend builds to `dist/public`
  2. Backend bundles to `dist/index.js`
- **Production**: Serves static files + API from single process
- **Development**: Concurrent frontend and backend with HMR

### Database Strategy
- **Development**: Local PostgreSQL instance
- **Production**: Neon serverless PostgreSQL
- **Migrations**: Drizzle Kit for schema management
- **Connection**: Environment-based configuration

### Performance Considerations
- **Code Splitting**: Vite handles automatic code splitting
- **Bundle Optimization**: ESBuild for efficient backend bundling
- **Database**: Connection pooling and query optimization ready
- **Caching**: React Query provides client-side caching

## Changelog
- June 21, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.