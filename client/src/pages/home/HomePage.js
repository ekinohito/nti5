import React from "react";
import Header from "./header/Header";
import Content from "./content/Content";
import Footer from "./footer/Footer";
import AuthModal from "./modals/AuthModal";

export const HomePage = () => {
    return (
        <div>
            <AuthModal/>
            <Header/>
            <Content/>
            <Footer/>
        </div>
    )
}