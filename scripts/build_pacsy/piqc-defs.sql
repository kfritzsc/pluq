DROP TABLE IF EXISTS `SEQ_CS_DB`;

CREATE TABLE `SEQ_CS_DB` (
  `KEY_ID` char(9) NOT NULL,
  `ELEMENT` char(1) NOT NULL,
  `C_OFF_MODE` double default NULL,
  `C_OFF_AVG` double default NULL,
  `C_OFF_STD` double default NULL,
  `C_COUNT` int(11) default NULL,
  `PIQC` tinyint(1) default NULL,
  KEY `IDX27` (`KEY_ID`),
  KEY `IDX2001` (`ELEMENT`),
  KEY `IDX2002` (`C_OFF_MODE`),
  KEY `IDX2003` (`C_OFF_AVG`),
  KEY `IDX2004` (`C_OFF_STD`),
  KEY `IDX2005` (`C_COUNT`),
  KEY `IDX2006` (`PIQC`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `CS_STATS_DB`;


CREATE TABLE `CS_STATS_DB` (
  `RES` char(1) NOT NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `SND_STRC` char(1) NOT NULL,
  `C_MODE` double default NULL,
  `C_AVG` double default NULL,
  `C_STD` double default NULL,
  `C_95MIN` double default NULL,
  `C_95MAX` double default NULL,
  KEY `IDX2011` (`Res`),
  KEY `IDX2012` (`ATOM_NAME`),
  KEY `IDX2014` (`SND_STRC`),
  KEY `IDX2015` (`C_MODE`),
  KEY `IDX2016` (`C_AVG`),
  KEY `IDX2017` (`C_STD`),
  KEY `IDX2018` (`C_95MIN`),
  KEY `IDX2019` (`C_95MAX`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;