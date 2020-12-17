import React from "react";
import logo from "../../../assets/logos/logo-onti.svg";
import {useDispatch} from "react-redux";
import {setAuthModalIsOpen} from "../../../actions";

const Header = () => {
    const dispatch = useDispatch();
    return (
        <div className="main-header d-flex px-3 py-1">
            <div className="flex-grow-1">
                <img src={logo} alt="logo"/>
            </div>
            <button className="btn btn-primary" onClick={() => dispatch(setAuthModalIsOpen(true))}>
                Войти
            </button>
        </div>
    )
}

export default Header;