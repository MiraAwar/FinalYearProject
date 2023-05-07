import React, { useState } from 'react';

function Table({ data, maturity }) {
    const rows = [];
    for (let i = 0; i < data.length; i++) {
      rows.push(
        <tr key={i}>
          <td>{data[i]}</td>
        </tr>
      );
    }
  
    return (
      <table>
        <thead>
          <tr>
            <th>Yields for maturity {maturity} years</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    );
  }

export default Table;