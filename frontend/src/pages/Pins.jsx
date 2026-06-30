import './Pins.css'
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PinCard from '../components/PinCard.jsx'

export default function Pins(){
    const [pins, setPins] = useState([]);
    const [error, setError] = useState('');
    useEffect(() => {
        const fetchData = async () => {
            const response = await axios.get('http://127.0.0.1:8000/api/pins/');
            if(response.status !== 200) {
                setError('Ошибка загрузки постов');
            }
            setPins(response.data);
        }; fetchData();
        const intervalId = setInterval(fetchData, 5000);
    }, []);
    return (
        <div>
            <h2 style={{paddingTop: "20px", marginBottom: "15px"}}>Опубликованные посты:</h2>
            {error &&
                <div>
                    {error}
                </div>
            }
            <div style={{marginInline: 'auto', width: 'fit-content'}}>
                <ul className="pins_list">
                    {pins.map(item => <li key={item.id}><PinCard pin={item}/></li>)}
                </ul>
            </div>
        </div>
    );
}