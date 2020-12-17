import React from "react";
import logo from "../../../assets/logos/logo-onti.svg";
import {useDispatch, useSelector} from "react-redux";
import {setAuthModalIsOpen, setUser} from "../../../actions";

const Header = () => {
    const dispatch = useDispatch();
    const user = useSelector(state => state.user);
    return (
        <div className="main-header d-flex px-3 py-1">
            <div className="flex-grow-1">
                <img src={logo} alt="logo"/>
            </div>
            {
                !user
                    ?
                    <button className="btn btn-primary" onClick={() => dispatch(setAuthModalIsOpen(true))}>
                        Войти
                    </button>
                    :
                    <button className="btn btn-danger" onClick={() => {
                        localStorage.removeItem('token');
                        dispatch(setUser(null))
                    }}>
                        Выйти
                    </button>
            }

        </div>
    )
}

export default Header;