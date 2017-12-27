/*----- 省份基础信息 -----*/
create table if not exists TProvinceBaseInfo(
	Name			VARCHAR(80),
	AlphaCode		VARCHAR(50)
)default charset=utf8;
/*
comment on table TProvinceBaseInfo
	is '省份基础信息';
comment on table TProvinceBaseInfo.AlphaCode
	is '省份拼音';
comment on table TProvinceBaseInfo.Name
	is '省份中文名';
*/

/*----- 城市基础信息 -----*/
create table if not exists TCityBaseInfo(
	CityID			integer primary key,
	Name			VARCHAR(30) not null,
	AlphaCode		VARCHAR(80),
	ProvinceCode	VARCHAR(50)
)default charset=utf8;
/*
comment on table TCityBaseInfo
	is '城市基础信息';
comment on table TCityBaseInfo.CityID
	is '城市唯一ID编号';
comment on table TCityBaseInfo.Name
	is '城市中文名';
comment on table TCityBaseInfo.AlphaCode
	is '城市名拼音';
comment on table TCityBaseInfo.ProvinceCode
	is '所属省份的拼音码';
*/

/*----- 风向基础信息 -----*/
create table if not exists TWindDirectionBaseInfo(
	WindID	integer primary key,
	Name	VARCHAR(10),
	Icon	VARCHAR(100)
)default charset=utf8;
/*
comment on table TWindDirectionBaseInfo
	is '风向基础信息';
comment on table TWindDirectionBaseInfo.WindID
	is '风向ID';
comment on table TWindDirectionBaseInfo.Name
	is '风向中文名称';
comment on table TWindDirectionBaseInfo.Icon
	is '对应图标路径';
*/

/*----- 天气基础信息 -----*/
create table if not exists TWindDirectionBaseInfo(
	WindID	integer primary key,
	Name	VARCHAR(10),
	Icon	VARCHAR(100)
)default charset=utf8;
/*
comment on table TWindDirectionBaseInfo
	is '天气基础信息';
comment on table TWindDirectionBaseInfo.WindID
	is '天气ID';
comment on table TWindDirectionBaseInfo.Name
	is '天气中文名称';
comment on table TWindDirectionBaseInfo.Icon
	is '对应图标路径';
*/

/*----- 按天天气信息 -----*/
create table if not exists TDayWeather(
	CityID			integer not null,
	WeatherDate		DATE,
	UpdateDT		DateTime,
	NowTemp			TINYINT,
	MaxTemp			TINYINT,
	MinTemp			TINYINT,
	Weather			VARCHAR(10),
	NowWindDirectionID	VARCHAR(10),
	StartWindDirectionID	VARCHAR(10),
	EndWindDirectionID		VARCHAR(10),
	WindScale				VARCHAR(10),
	Humidity				FLOAT,
	AQI						VARCHAR(20),
	primary key(CityID, WeatherDate)
)default charset=utf8;
/*
comment on table TDayWeather
	is '按天天气信息';
comment on table TDayWeather.CityID
	is '城市ID';
comment on table TDayWeather.WeatherDate
	is '天气日期';
comment on table TDayWeather.UpdateDT
	is '最后更新日期';
comment on table TDayWeather.NowTemp
	is '当前温度';
comment on table TDayWeather.MaxTemp
	is '当天最高温度';
comment on table TDayWeather.MinTemp
	is '当天最低温度';
comment on table TDayWeather.Weather
	is '天气';
comment on table TDayWeather.NowWindDirectionID
	is '当前风向';
comment on table TDayWeather.StartWindDirectionID
	is '当天起始风向';
comment on table TDayWeather.EndWindDirectionID
	is '当天结束风向';
comment on table TDayWeather.WindScale
	is '风级';
comment on table TDayWeather.Humidity
	is '湿度';
comment on table TDayWeather.AQI
	is '空气质量信息';
*/

/*----- 分时天气信息 -----*/
create table if not exists TDetailWeather(
	CityID		integer not null,
	WeatherTime	DateTime,
/*	UpdateDT	DateTime, */
	Temp		TINYINT,
	Weather		VARCHAR(10),
	primary key(CityID, WeatherTime)
)default charset=utf8;
/*
comment on table TDetailWeather
	is '分时天气信息';
comment on table TDetailWeather.CityID
	is '城市ID';
comment on table TDetailWeather.WeatherTime
	is '时间点'；
comment on table TDetailWeather.UpdateDT
	is '最后更新日期'；
comment on table TDetailWeather.Temp
	is '该时间点的温度';
comment on table TDetailWeather.Weather
	is '该时间点的天气';
*/
create table if not exists TAQIInfo(
	CityID integer not null,
	WeatherDate	DATE,
	UpdateDT	DateTime,
	AQI			SMALLINT,
	PM10		SMALLINT,
	PM25		SMALLINT,
	NO2			SMALLINT,
	SO2			SMALLINT,
	CO			FLOAT(2,1),
	O3			SMALLINT,
	primary key(CityID, WeatherDate)
)default charset=utf8;
/*
comment on table TAQIInfo
	is 'AQI详细信息表';
comment on table TAQIInfo.CityID
	is '城市ID';
comment on table TAQIInfo.WeatherDate
	is 'AQI日期';
comment on table TAQIInfo.UpdateDT
	is '最后更新时间';
comment on table TAQIInfo.AQI
	is 'AQI综合指数';
comment on table TAQIInfo.PM10
	is 'PM10指数';
comment on table TAQIInfo.PM25
	is 'PM2.5指数';
comment on table TAQIInfo.NO2
	is '二氧化氮指数';
comment on table TAQIInfo.SO2
	is '二氧化硫指数';
comment on table TAQIInfo.CO
	is '一氧化碳指数';
comment on table TAQIInfo.O3
	is '臭氧指数';	
*/
create table if not exists TUpdateRecord(
	CityID			integer primary key,
	LastUpdateDT	DateTime
)default charset=utf8;
/*
comment on table TUpdateRecord
	is '数据的最后更新时间'；
comment on table TUpdateRecord.CityID
	is '城市ID'；
comment on table TUpdateRecord.LastUpdateDT
	is '信息最后更新时间';
*/