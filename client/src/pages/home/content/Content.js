import React, {useEffect} from "react";
import tour from "../../../assets/logos/tour.svg"
import {fetchGames, setAuthModalIsOpen, setModalMethod, setNicknameModalIsOpen} from "../../../actions";
import {useDispatch, useSelector} from "react-redux";

const Content = () => {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(fetchGames())
    }, [dispatch]);

    const games = useSelector(state => state.games);

    return (
        <div className="main-content p-3">
            {
                games.map((value, index) => (
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

                                    <button type="button" className="btn btn-danger main-item-description"
                                            onClick={
                                                () => {
                                                    console.log(value)
                                                    dispatch(setModalMethod(value.method))
                                                    dispatch(setNicknameModalIsOpen(true));
                                                }
                                            }>Добавить аккаунт</button>

                                </div>
                        }

                    </div>
                ))
            }
        </div>
    )
}

export default Content;