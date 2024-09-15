import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {
  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <div className='App-header'>
        <h1
          onClick={() => {
            this.navTo('');
          }}
          className='clickable'
        >
          Udacitrivia
        </h1>
        <h2
          onClick={() => {
            this.navTo('');
          }}
          className='clickable'
        >
          List
        </h2>
        <h2
          onClick={() => {
            this.navTo('/add');
          }}
          className='clickable'
        >
          Add
        </h2>
        <h2
          onClick={() => {
            this.navTo('/play');
          }}
          className='clickable'
        >
          Play
        </h2>
      </div>
    );
  }
}

export default Header;
