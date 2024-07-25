"use strict";

const { Model, DataTypes } = require("sequelize");

module.exports = (sequelize) => {
  class Location extends Model {
    
  }

  Location.init(
    {
      uid: {
        type: DataTypes.INTEGER,
        unique: true,
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
      },
      loca_x: {
        type: DataTypes.FLOAT,
        allowNull: false,
      },
      loca_y: {
        type: DataTypes.FLOAT,
        allowNull: false,
      },
      loca_z: {
        type: DataTypes.FLOAT,
        allowNull: false,
      },
      slope: {
        type: DataTypes.FLOAT,
      },
      chim_name: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
      },
      
    },
    {
      sequelize,
      modelName: "Location",
    }
  );

  return Location;
};
