import './App.css';
import React, { useState } from "react";
import axios from 'axios';
import config from 'config.json';
import Modal from 'react-modal';

const ModalStyle = {
  overlay: {
    background: "#e9e3f2b0"
  },
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    background: '#e3dcef',
    transform: 'translate(-50%, -50%)',
  },
};

function App() {
  document.title = "Fotobox";

  function delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  const [pic_open, setPicOpen] = useState(false);
  const [pic_id, setPicId] = useState<String | null>(null);

  const [qr_open, setQrOpen] = useState(false);
  const [qr_url, setQrUrl] = useState<string | null>(null);
  const [qr_source, setQrSource] = useState<string | null>(null);

  const [countdown_running, setCountdownRunning] = useState(false);
  const [countdown_text, setCountdownText] = useState("3");

  function foto_machen() {
    setCountdownRunning(true);
    (async () => {
      setCountdownText("3");
      await delay(1000);
      setCountdownText("2");
      await delay(1000);
      setCountdownText("1");
      await delay(1000);
      setCountdownText("Cheese!");
      await delay(200);

      axios.post(`${config.api_endpoint}/foto`)
        .then((response) => {
          //clear
          setQrSource(null);
          setQrUrl(null);

          setPicId(response.data["id"]);
          setPicOpen(true);
          setCountdownRunning(false);
        })
        .catch((error) => {
          console.error(error);
          alert("Ein Fehler ist aufgetreten!");
          setPicId("0");
          setPicOpen(true);
          setCountdownRunning(false);
        });

    })();
  }

  const validateEmail = (email: any) => {
    return email.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
  };

  function foto_teilen(methode: String) {
    if (methode === "email") {
      const email = prompt("Bitte geben Sie ihre E-Mail Adresse ein:")
      if (!email) {
        return
      } if (!validateEmail(email)) {
        alert("E-Mail ist nicht korrekt!")
        return
      }

      axios.post(`${config.api_endpoint}/teilen`, { methode: methode, id: pic_id, mail: email })
        .then((response) => {
          alert("E-Mail wurde versendet!")
        })
        .catch((error) => {
          console.error(error);
          alert("Ein Fehler ist aufgetreten!");
        });

    } if (methode === "qr") {
      axios.post(`${config.api_endpoint}/teilen`, { methode: methode, id: pic_id })
        .then((response) => {
          setQrUrl(response.data["url"]);
          setQrOpen(true);
        })
        .catch((error) => {
          console.error(error);
          alert("Ein Fehler ist aufgetreten!");
        });
    }
  }

  return (
    <div>

      <div className='text infobox'>
        <div className='center'>
          <h1>SIND SIE BEREIT?</h1>
          <h1>DANN BETÄTIGEN SIE JETZT DEN AUSLÖSER!</h1>
        </div>
      </div>
      <div className='center'>
        {countdown_running ? (
          <h1>{countdown_text}</h1>
        ) : (
          <button className='button-foto' onClick={() => foto_machen()}>Foto machen!*</button>
        )}
      </div>

      <div className='infobox center footer'>
        <h4>*Datenschutz</h4>
        <p>Mit der Nutzung dieses Dienstes stimme Sie zu, <br /> dass die Bilder, die durch diese Fotobox erstellt werden, zur Weiterleitung zu mir auf einer <br /> externen -nicht öffentlich zugänglichen- Website etwa 30 Tage gespeichert und gegebenenfalls verarbeitet werden. <br /> Wenn Sie NICHT EINVERSTANDEN sind, bitten wir darum, diesen Dienst nicht zu verwenden.</p>
        <br />
        <p>made with ❤ by Easy Tec & Jonny Tutorials</p>
      </div>

      <Modal
        isOpen={pic_open}
        style={ModalStyle}
        contentLabel="Foto"
        onRequestClose={() => setPicOpen(false)}
      >
        <button onClick={() => setPicOpen(false)} className='button-schließen'>Schließen</button>
        {pic_id ? (
          <div className='flex'>
            <div>
              <button className='button-teilen' onClick={() => foto_teilen("email")}><img src="/img/email.png" className='button-teilen-img' /></button>
              <br />
              <button className='button-teilen' onClick={() => foto_teilen("qr")}><img src="/img/qr-code.png" className='button-teilen-img' /></button>
            </div>

            <img className='rounded' src={`${config.api_endpoint}/fotos/${pic_id}.jpg`} width={900} height={600} />
          </div>
        ) : <></>}
      </Modal>

      <Modal
        isOpen={qr_open}
        style={ModalStyle}
        contentLabel="Foto"
        onRequestClose={() => setQrOpen(false)}
      >
        <button onClick={() => setQrOpen(false)} className='button-schließen'>Schließen</button>
        {qr_url ? (
          <div>
            <img className='rounded' src={qr_url} width={400} height={400} />
          </div>
        ) : <></>}
      </Modal>

    </div>
  );
}

export default App;
