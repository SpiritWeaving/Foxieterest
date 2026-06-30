import React, { createContext, useState, useContext, useEffect } from 'react';
import authService from '../services/authService';
import api from '../services/api';

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);
export const AuthProvider = ({ children }) => {
    // Текущий пользователь
    const [user, setUser] = useState(null);
    // state загрузки
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        // Проверяем сохраненного пользователя при загрузке
        const currentUser = authService.getCurrentUser();
        const isAuthenticated = authService.isAuthenticated();
        if (currentUser && isAuthenticated) {
            setUser(currentUser);
        }
        setLoading(false);
    }, []);

const register = async (username, email, password, password2) => {
    try {
        await authService.register(username, email, password, password2);
        // После регистрации выполняем вход
        return await login(username, password);
    } catch (error) {
        throw error;
    }
};

const login = async (username, password) => {
    try {
        // Сначала получаем JWT токены
        await authService.getTokens(username, password);
        // Затем получаем данные пользователя
        const response = await api.post('/auth/login/', { username, password
        });
        if (response.data.user) {
            setUser(response.data.user);
            return { success: true };
        }
        return { success: false, error: 'Ошибка входа' };
    } catch (error) {
        return {
            success: false,
            error: error.response?.data?.detail || 'Ошибка входа'
        };
    }
};

const logout = () => {
    authService.logout();
    setUser(null);
};

const value = {
    user,
    loading,
    register,
    login,
    logout,
    isAuthenticated: !!user && authService.isAuthenticated()
};

return (
    <AuthContext.Provider value={value}>
    {children}
    </AuthContext.Provider>
    );
};