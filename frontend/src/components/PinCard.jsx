import './PinCard.css'
import React, {useState} from 'react'

export default function PinCard({pin}){
    const boards = pin.boards;
    const [likes, setLikes] = useState(pin.liked_by);
    return (
        <div className="pin__card">
            <div className="pin__content">
                {pin.is_image &&
                    <img src={pin.content}
                    className="pin__content__img"
                    alt="Содержимое поста"/>
                }
                {pin.is_video &&
                    <video className="pin__content__video" muted
                    alt="Содержимое поста" controls>
                     <source src={pin.content} type="video/mp4"/>
                    </video>
                }
            </div>
            <div className="pin__description_container">
                <h3 className="pin__title">{pin.title}</h3>
                <p>Лайки: {likes.length}</p>
{/*             <ul style={{marginLeft: "0", paddingLeft: "0", */}
{/*                 display: "flex", gap: "5px"}}> */}
{/*                 <p>Сохранен на досках:</p> */}
{/*                 <div style={{display: "flex", gap: "5px"}}> */}
{/*                 {boards.map(item => { */}
{/*                     return ( */}
{/*                         <li style={{listStyleType: "none"}}> */}
{/*                             <a>{item}</a> */}
{/*                         </li> */}
{/*                     ); */}
{/*                 })} */}
{/*                 </div> */}
{/*             </ul> */}
            </div>
        </div>
    );
}