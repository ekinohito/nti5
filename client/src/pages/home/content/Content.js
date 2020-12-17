import React, {useEffect} from "react";
import tour from "../../../assets/logos/tour.svg"
import {fetchGames} from "../../../actions";
import {useDispatch, useSelector} from "react-redux";

const Content = () => {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(fetchGames())
    }, [dispatch]);

    const games = useSelector(state => state.games)

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
                                            data-toggle="modal" data-target={`#${value.title}`}>Добавить аккаунт</button>

                                    <div className="modal fade" id={value.title} tabIndex="-1" role="dialog">
                                        <div className="modal-dialog" role="document">
                                            <div className="modal-content">
                                                <div className="modal-header">
                                                    <button type="button" className="close" data-dismiss="modal"
                                                            aria-label="Close">
                                                        <span aria-hidden="true">&times;</span>
                                                    </button>
                                                    <h4 className="modal-title" id="myModalLabel">Modal title</h4>
                                                </div>
                                                <div className="modal-body">
                                                    ...
                                                </div>
                                                <div className="modal-footer">
                                                    <button type="button" className="btn btn-secondary"
                                                            data-dismiss="modal">Close
                                                    </button>
                                                    <button type="button" className="btn btn-primary">Save changes
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                        }

                    </div>
                ))
            }
        </div>
    )
}

export default Content;