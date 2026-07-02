import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';
import PublicRoute from './components/PublicRoute'; import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import Pins from './pages/Pins';
import Footer from './components/Footer';
import Navbar from './components/Navbar';

import './assets/fonts/fonts.css'

function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <Navbar />
                <Routes>
                    <Route path="/login" element={
                        <PublicRoute>
                            <LoginForm />
                        </PublicRoute>
                    } />
                    <Route path="/register" element={
                        <PublicRoute>
                            <RegisterForm />
                        </PublicRoute>
                    } />
                    <Route path="/pins" element={
                        <PrivateRoute>
                            <Pins />
                        </PrivateRoute>
                    } />
                    <Route path="/" element={
                        <PrivateRoute>
                            <Pins />
                        </PrivateRoute>
                    } />
                </Routes>
                <Footer />
            </AuthProvider>
        </BrowserRouter>
    );
}
export default App;