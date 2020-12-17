import React, {useState} from 'react';
import {useDispatch, useSelector} from "react-redux";
import ModalPopup from "../../../containers/ModalPopup";
import {apiRequest} from "../../../http";
import {fetchGames, setNicknameModalIsOpen} from "../../../actions";

const NicknameModal = ( ) => {
    const dispatch = useDispatch();
    const isOpen = useSelector(state => state.nicknameModalIsOpen);
    const method = useSelector(state => state.modalMethod);
    console.log(method)

    const [username, setUsername] = useState('');

    return (
        <ModalPopup isOpen={isOpen}>
            <div className="form-group">
                <span>Идентификационные данные</span>
                <input type="text" className="form-control mt-2" value={username} onChange={(e) => setUsername(e.target.value)}/>
            </div>

            <div className="form-group d-flex justify-content-between">
                <button className="btn btn-primary" onClick={
                    () =>
                        apiRequest(method, 'POST', true, {
                            payload: username
                        })
                            .then(res => res.text())
                            .then(text => {
                                dispatch(setNicknameModalIsOpen(false));
                                dispatch(fetchGames());
                            })
                }>
                    Ввести
                </button>
            </div>
        </ModalPopup>
    );
};

export default NicknameModal;