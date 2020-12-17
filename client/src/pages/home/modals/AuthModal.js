import React, {useState} from 'react';
import {useDispatch, useSelector} from "react-redux";
import ModalPopup from "../../../containers/ModalPopup";
import {apiRequest} from "../../../http";
import {setAuthModalIsOpen} from "../../../actions";

const AuthModal = () => {
    const dispatch = useDispatch();
    const isOpen = useSelector(state => state.authModalIsOpen);

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    return (
        <ModalPopup isOpen={isOpen}>
            <div className="form-group">
                <span>Имя пользователя</span>
                <input type="text" className="form-control mt-2" value={username} onChange={(e) => setUsername(e.target.value)}/>
            </div>

            <div className="form-group">
                <span>Пароль</span>
                <input type="text" className="form-control mt-2" value={password} onChange={(e) => setPassword(e.target.value)}/>
            </div>

            <div className="form-group d-flex justify-content-between">
                <button className="btn btn-primary" onClick={
                    () =>
                        apiRequest("/user/login", 'POST', false, {
                            username, password
                        })
                            .then(res => res.text())
                            .then(text => {
                                localStorage.setItem("token", text);
                                dispatch(setAuthModalIsOpen(false));
                            })
                }>
                    Войти
                </button>
                <button className="btn btn-outline-primary">Регистрация</button>
            </div>
        </ModalPopup>
    );
};

export default AuthModal;