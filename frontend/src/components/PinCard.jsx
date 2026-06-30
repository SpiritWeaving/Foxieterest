import './PinCard.css'

export default function PinCard({pin}){
    const boards = pin.boards;
    return (
        <div className="pin__card">
            <div className="pin__content">
                {pin.is_image &&
                    <img src={pin.content}
                    className="pin__content__img"
                    alt="Содержимое поста"/>
                }
            </div>
            <div className="pin__description_container">
            <h3 className="pin__title">{pin.title}</h3>
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