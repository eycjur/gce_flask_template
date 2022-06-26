USE weather_db;
SHOW tables;

DROP TABLE IF EXISTS weather_log;

-- テーブル作成
CREATE TABLE weather_log(
    id INT NOT NULL AUTO_INCREMENT,
    date DATE NOT NULL UNIQUE,
    value FLOAT NOT NULL,
    PRIMARY KEY (`id`)
);
SHOW FULL COLUMNS FROM weather_log;

-- サンプルデータの挿入
INSERT INTO weather_log set	date='2022-01-01', value=1.2;
INSERT INTO weather_log set	date='2022-04-05', value=-4;
INSERT INTO weather_log set	date='2022-04-23', value=24;
INSERT INTO weather_log set	date='2022-07-12', value=6.1;
INSERT INTO weather_log set	date='2022-12-25', value=2.7;

-- 取得
SELECT  *
FROM weather_log
;
