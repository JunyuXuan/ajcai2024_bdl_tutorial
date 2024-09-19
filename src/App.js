import React, { Component } from "react";

import uwa_logo from "./images/uwacrest-blue.png";

import centre_logo from "./images/center-logo.png";
import nlp_tlp_logo from "./images/nlp-tlp-logo.png";
import "./App.scss";

import HomePage from "./pages/home";
import Hero from "./components/hero";

class Header extends Component {
  render() {
    return (
      <header className="header">
        <div className="container flex-container flex-align-center justify-space-between">
          <div class="header-left flex-container flex-align-center">
            <ul className="header-nav">
              <li>
                <a href="#abstract">Abstract </a>
              </li>
              <li>
                <a href="#outline">Outline</a>
              </li>
              <li>
                <a href="#venue">Venue</a>
              </li>
              <li>
                <a href="#what-to-bring">What to Bring</a>
              </li>
              <li>
                <a href="#materials">Materials</a>
              </li>
              <li>
                <a href="#speakers">Speaker</a>
              </li>
            </ul>
          </div>
          <div className="header-right flex-container flex-align-center">
            <div className="logo-group">
              <a href="https://maintenance.org.au">
                <div class="logo center-logo">
                  <img src={centre_logo} alt="NLP-TLP Logo" />
                </div>
              </a>
              <a href="https://uwa.edu.au" target="_blank" rel="noreferrer">
                <div class="logo">
                  <img src={uwa_logo} className="App-logo" alt="UWA logo" />
                </div>
              </a>
              <a href="https://nlp-tlp.org">
                <div class="logo nlp-tlp-logo">
                  <img src={nlp_tlp_logo} alt="NLP-TLP Logo" />
                </div>
              </a>
            </div>
          </div>
        </div>
      </header>
    );
  }
}
/*
<div className="logo-text">
  <h2>
    UWA Natural & Technical<br/>
    Language Processing
  </h2>
</div>
*/

class Footer extends Component {
  render() {
    return (
      <footer>
        <div className="container">
          <p>&copy; Website by Michael Stewart.</p>
        </div>
      </footer>
    );
  }
}

class App extends Component {
  render() {
    return (
      <>
        <Header />
        <Hero />
        <main id="main" className="container">
          <HomePage />
        </main>
        <Footer />
      </>
    );
  }
}

export default App;
