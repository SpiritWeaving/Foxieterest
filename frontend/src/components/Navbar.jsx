import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
const Navbar = () => {
    const { isAuthenticated, user, logout } = useAuth();
    const navigate = useNavigate();
    const handleLogout = () => {
        logout();
        navigate('/login');
    };
    return (
        <AppBar position="static" sx={{ backgroundColor: '#7793a1', boxShadow: 'none' }}>
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    <Link to="/" style={{
                        color: 'white', textDecoration: 'none'
                    }}>
                        Foxieterest
                    </Link>
                </Typography>
                {isAuthenticated ? (
                    <Box>
                        <Typography variant="body1" component="span" sx={{
                            mr: 2
                        }}>
                            <img src={`http://127.0.0.1:8000${user?.avatar}`}
                            style={{borderRadius: '50%', width: '40px',
                                height: '40px', objectFit: 'cover'}}/>
                            {user?.username}
                        </Typography>
                        <Button color="inherit" onClick={handleLogout}>
                            Выйти
                        </Button>
                    </Box>
                ) : (
                    <Box>
                        <Button color="inherit" component={Link} to="/login">
                            Вход
                        </Button>
                        <Button color="inherit" component={Link} to="/register">
                            Регистрация
                        </Button>
                    </Box>
                )}
            </Toolbar>
        </AppBar>
    );
};
export default Navbar;