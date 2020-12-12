import React, {useEffect, useState} from "react";
import tour from "../../../assets/logos/tour.svg"
import getGames from "../../../actions/actions";

const Content = () => {
    const [items, setItems] = useState([]);
    useEffect(() => {
        getGames(setItems)
    }, [setItems])

    return (
        <div className="main-content p-3">
            {
                items.map((value, index) => (
                    <div className={`container row align-items-center main-item p-5 m-3 ${value.presented ? "blue":"red"}`} key={index}>
                        <div className="col main-item-title mb-2">
                            {value.title}
                        </div>
                        <div className="justify-content-center col main-item-description mb-2">
                            {value.description}
                        </div>
                        {
                            value.presented?
                                <div className="col main-item-points text-right mb-2">
                                    <img src={tour} alt="tour" className="mx-2"/>
                                    {value.points}
                                </div>
                                :
                                <div className="col text-right mt-md-0 mt-5">
                                    <button className="btn btn-danger main-item-description">Добавить аккаунт</button>
                                </div>
                        }

                    </div>
                ))
            }
        </div>
    )
}

export default Content;