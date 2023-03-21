import React from "react";

function Example() {
    return (
      <Chosen onChange={value => console.log(value)}>
        <option>vanilla</option>
        <option>chocolate</option>
        <option>strawberry</option>
      </Chosen>
    );
  }

  class Chosen extends React.Component {
    render() {
      return (
        <div>
          <select className="Chosen-select" ref={el => this.el = el}>
            {this.props.children}
          </select>
        </div>
      );
    }
  }