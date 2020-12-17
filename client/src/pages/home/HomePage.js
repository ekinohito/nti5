import React from "react";
import Header from "./header/Header";
import Content from "./content/Content";
import Footer from "./footer/Footer";
import AuthModal from "./modals/AuthModal";
import NicknameModal from "./modals/NicknameModal";

export const HomePage = () => {
    return (
        <div>
            <AuthModal/>
            <NicknameModal/>
            <Header/>
            <Content/>
            <Footer/>
        </div>
    )
}