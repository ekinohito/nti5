import React from 'react';
import Modal from 'react-modal';

import styles from './containers.module.css';
import {closeAllModals} from "../actions";
import {useDispatch} from "react-redux";


const style = {
    overlay: {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(14, 14, 14, 0.32)',
        overflow: 'hidden',
        zIndex: 1000
    },
    content: {
        margin: 0,
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'transparent',
        padding: 0
    }
};

const ModalPopup = ({isOpen, ...props}) => {
    const width = props.width ?? 350;

    const dispatch = useDispatch();

    return (
        <Modal
            isOpen={isOpen}
            style={style}
            closeTimeoutMS={300}
        >
            <div className="container" style={{height: '100%'}}>
                <div className="d-flex justify-content-center align-items-center" style={{height: '100%'}}>
                    <div style={{width}} className={`${styles.modalBody} p-4 bg-light`}>
                        <div className="d-flex justify-content-end">
                            <button onClick={() => dispatch(closeAllModals())} className="btn btn-outline-danger">
                                Закрыть
                            </button>
                        </div>
                        {props.children}
                    </div>
                </div>
            </div>

        </Modal>
    )
}

export default ModalPopup;