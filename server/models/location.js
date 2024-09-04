"use strict";

const { Model, DataTypes, Op } = require("sequelize");

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
        type: DataTypes.DECIMAL(40, 20),
        allowNull: false,
      },
      loca_y: {
        type: DataTypes.DECIMAL(40, 20),
        allowNull: false,
      },
      loca_z: {
        type: DataTypes.DECIMAL(40, 20),
        allowNull: false,
      },
      slope: {
        type: DataTypes.DECIMAL(40, 20),
      },
      chim_name: {
        type: DataTypes.STRING,
        allowNull: false,
      },
      chim_num: {
        type: DataTypes.INTEGER,
        allowNull: false,
      },
      
    },
    {
      sequelize,
      modelName: "Location",
      hooks: {
        // beforeCreate 후크는 레코드가 생성되기 전에 실행됨
        beforeCreate: async (location, options) => {
          // 같은 chim_name을 가진 레코드 중 가장 높은 chim_num 값을 찾음
          const maxChimNum = await Location.max('chim_num', {
            where: {
              chim_name: location.chim_name // 현재 입력하려는 chim_name과 동일한 레코드들 중에서 찾음
            }
          });

          // 만약 maxChimNum 값이 존재하면 +1, 없으면(즉, 첫 레코드인 경우) 1로 설정
          location.chim_num = maxChimNum !== null ? maxChimNum + 1 : 1;
        },
      },
    }
  );

  return Location;
};
