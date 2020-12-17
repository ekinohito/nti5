import React from 'react';
import Modal from 'react-modal';

import "./containers.scss";

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
    return (
        <Modal
            isOpen={isOpen}
            style={style}
            closeTimeoutMS={300}
        >
            <div className="container" style={{height: '100%'}}>
                <div className="d-flex justify-content-center align-items-center" style={{height: '100%'}}>
                    <div className="modal-lg flex-grow-1 flex-shrink-1">
                        {props.children}
                    </div>

                </div>
            </div>

        </Modal>
    )
}

export default ModalPopup;