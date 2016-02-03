-- MySQL dump 10.11
--
-- Host: localhost    Database: pacsy
-- ------------------------------------------------------
-- Server version	5.0.95

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `A_COORD_DB`
--

DROP TABLE IF EXISTS `A_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `A_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX25` (`MODEL_NO`),
  KEY `IDX26` (`KEY_ID`),
  KEY `IDX27` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `A_CS_DB`
--

DROP TABLE IF EXISTS `A_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `A_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX28` (`ATOM_NAME`),
  KEY `IDX29` (`C_SHIFT`),
  KEY `IDX30` (`AMBIGUITY`),
  KEY `IDX31` (`KEY_ID`),
  KEY `IDX32` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `A_DB`
--

DROP TABLE IF EXISTS `A_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `A_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX33` (`CHAIN_ID`),
  KEY `IDX34` (`SEQ_ID`),
  KEY `IDX35` (`SEQ_NAME`),
  KEY `IDX36` (`KEY_ID`),
  KEY `IDX37` (`FIRSTKEY_ID`),
  KEY `IDX1000` (`PREV_X`),
  KEY `IDX1001` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `A_STRC_DB`
--

DROP TABLE IF EXISTS `A_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `A_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX16` (`SND_STRC`),
  KEY `IDX17` (`EDGE`),
  KEY `IDX18` (`PHI`),
  KEY `IDX19` (`PSI`),
  KEY `IDX20` (`HDO_PBT`),
  KEY `IDX21` (`SAS`),
  KEY `IDX22` (`MODEL_NO`),
  KEY `IDX23` (`KEY_ID`),
  KEY `IDX24` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `C_COORD_DB`
--

DROP TABLE IF EXISTS `C_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `C_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX113` (`MODEL_NO`),
  KEY `IDX114` (`KEY_ID`),
  KEY `IDX115` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `C_CS_DB`
--

DROP TABLE IF EXISTS `C_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `C_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX116` (`ATOM_NAME`),
  KEY `IDX117` (`C_SHIFT`),
  KEY `IDX118` (`AMBIGUITY`),
  KEY `IDX119` (`KEY_ID`),
  KEY `IDX120` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `C_DB`
--

DROP TABLE IF EXISTS `C_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `C_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX121` (`CHAIN_ID`),
  KEY `IDX122` (`SEQ_ID`),
  KEY `IDX123` (`SEQ_NAME`),
  KEY `IDX124` (`KEY_ID`),
  KEY `IDX125` (`FIRSTKEY_ID`),
  KEY `IDX1008` (`PREV_X`),
  KEY `IDX1009` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `C_STRC_DB`
--

DROP TABLE IF EXISTS `C_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `C_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX104` (`SND_STRC`),
  KEY `IDX105` (`EDGE`),
  KEY `IDX106` (`PHI`),
  KEY `IDX107` (`PSI`),
  KEY `IDX108` (`HDO_PBT`),
  KEY `IDX109` (`SAS`),
  KEY `IDX110` (`MODEL_NO`),
  KEY `IDX111` (`KEY_ID`),
  KEY `IDX112` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `D_COORD_DB`
--

DROP TABLE IF EXISTS `D_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `D_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX91` (`MODEL_NO`),
  KEY `IDX92` (`KEY_ID`),
  KEY `IDX93` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `D_CS_DB`
--

DROP TABLE IF EXISTS `D_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `D_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX94` (`ATOM_NAME`),
  KEY `IDX95` (`C_SHIFT`),
  KEY `IDX96` (`AMBIGUITY`),
  KEY `IDX97` (`KEY_ID`),
  KEY `IDX98` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `D_DB`
--

DROP TABLE IF EXISTS `D_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `D_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX99` (`CHAIN_ID`),
  KEY `IDX100` (`SEQ_ID`),
  KEY `IDX101` (`SEQ_NAME`),
  KEY `IDX102` (`KEY_ID`),
  KEY `IDX103` (`FIRSTKEY_ID`),
  KEY `IDX1006` (`PREV_X`),
  KEY `IDX1007` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `D_STRC_DB`
--

DROP TABLE IF EXISTS `D_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `D_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX82` (`SND_STRC`),
  KEY `IDX83` (`EDGE`),
  KEY `IDX84` (`PHI`),
  KEY `IDX85` (`PSI`),
  KEY `IDX86` (`HDO_PBT`),
  KEY `IDX87` (`SAS`),
  KEY `IDX88` (`MODEL_NO`),
  KEY `IDX89` (`KEY_ID`),
  KEY `IDX90` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `E_COORD_DB`
--

DROP TABLE IF EXISTS `E_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `E_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX157` (`MODEL_NO`),
  KEY `IDX158` (`KEY_ID`),
  KEY `IDX159` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `E_CS_DB`
--

DROP TABLE IF EXISTS `E_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `E_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX160` (`ATOM_NAME`),
  KEY `IDX161` (`C_SHIFT`),
  KEY `IDX162` (`AMBIGUITY`),
  KEY `IDX163` (`KEY_ID`),
  KEY `IDX164` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `E_DB`
--

DROP TABLE IF EXISTS `E_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `E_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX165` (`CHAIN_ID`),
  KEY `IDX166` (`SEQ_ID`),
  KEY `IDX167` (`SEQ_NAME`),
  KEY `IDX168` (`KEY_ID`),
  KEY `IDX169` (`FIRSTKEY_ID`),
  KEY `IDX1012` (`PREV_X`),
  KEY `IDX1013` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `E_STRC_DB`
--

DROP TABLE IF EXISTS `E_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `E_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX148` (`SND_STRC`),
  KEY `IDX149` (`EDGE`),
  KEY `IDX150` (`PHI`),
  KEY `IDX151` (`PSI`),
  KEY `IDX152` (`HDO_PBT`),
  KEY `IDX153` (`SAS`),
  KEY `IDX154` (`MODEL_NO`),
  KEY `IDX155` (`KEY_ID`),
  KEY `IDX156` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `F_COORD_DB`
--

DROP TABLE IF EXISTS `F_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `F_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX311` (`MODEL_NO`),
  KEY `IDX312` (`KEY_ID`),
  KEY `IDX313` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `F_CS_DB`
--

DROP TABLE IF EXISTS `F_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `F_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX314` (`ATOM_NAME`),
  KEY `IDX315` (`C_SHIFT`),
  KEY `IDX316` (`AMBIGUITY`),
  KEY `IDX317` (`KEY_ID`),
  KEY `IDX318` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `F_DB`
--

DROP TABLE IF EXISTS `F_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `F_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX319` (`CHAIN_ID`),
  KEY `IDX320` (`SEQ_ID`),
  KEY `IDX321` (`SEQ_NAME`),
  KEY `IDX322` (`KEY_ID`),
  KEY `IDX323` (`FIRSTKEY_ID`),
  KEY `IDX1026` (`PREV_X`),
  KEY `IDX1027` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `F_STRC_DB`
--

DROP TABLE IF EXISTS `F_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `F_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX302` (`SND_STRC`),
  KEY `IDX303` (`EDGE`),
  KEY `IDX304` (`PHI`),
  KEY `IDX305` (`PSI`),
  KEY `IDX306` (`HDO_PBT`),
  KEY `IDX307` (`SAS`),
  KEY `IDX308` (`MODEL_NO`),
  KEY `IDX309` (`KEY_ID`),
  KEY `IDX310` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `G_COORD_DB`
--

DROP TABLE IF EXISTS `G_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `G_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX179` (`MODEL_NO`),
  KEY `IDX180` (`KEY_ID`),
  KEY `IDX181` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `G_CS_DB`
--

DROP TABLE IF EXISTS `G_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `G_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX182` (`ATOM_NAME`),
  KEY `IDX183` (`C_SHIFT`),
  KEY `IDX184` (`AMBIGUITY`),
  KEY `IDX185` (`KEY_ID`),
  KEY `IDX186` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `G_DB`
--

DROP TABLE IF EXISTS `G_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `G_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX187` (`CHAIN_ID`),
  KEY `IDX188` (`SEQ_ID`),
  KEY `IDX189` (`SEQ_NAME`),
  KEY `IDX190` (`KEY_ID`),
  KEY `IDX191` (`FIRSTKEY_ID`),
  KEY `IDX1014` (`PREV_X`),
  KEY `IDX1015` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `G_STRC_DB`
--

DROP TABLE IF EXISTS `G_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `G_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX170` (`SND_STRC`),
  KEY `IDX171` (`EDGE`),
  KEY `IDX172` (`PHI`),
  KEY `IDX173` (`PSI`),
  KEY `IDX174` (`HDO_PBT`),
  KEY `IDX175` (`SAS`),
  KEY `IDX176` (`MODEL_NO`),
  KEY `IDX177` (`KEY_ID`),
  KEY `IDX178` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `H_COORD_DB`
--

DROP TABLE IF EXISTS `H_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `H_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX201` (`MODEL_NO`),
  KEY `IDX202` (`KEY_ID`),
  KEY `IDX203` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `H_CS_DB`
--

DROP TABLE IF EXISTS `H_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `H_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX204` (`ATOM_NAME`),
  KEY `IDX205` (`C_SHIFT`),
  KEY `IDX206` (`AMBIGUITY`),
  KEY `IDX207` (`KEY_ID`),
  KEY `IDX208` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `H_DB`
--

DROP TABLE IF EXISTS `H_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `H_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX209` (`CHAIN_ID`),
  KEY `IDX210` (`SEQ_ID`),
  KEY `IDX211` (`SEQ_NAME`),
  KEY `IDX212` (`KEY_ID`),
  KEY `IDX213` (`FIRSTKEY_ID`),
  KEY `IDX1016` (`PREV_X`),
  KEY `IDX1017` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `H_STRC_DB`
--

DROP TABLE IF EXISTS `H_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `H_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX192` (`SND_STRC`),
  KEY `IDX193` (`EDGE`),
  KEY `IDX194` (`PHI`),
  KEY `IDX195` (`PSI`),
  KEY `IDX196` (`HDO_PBT`),
  KEY `IDX197` (`SAS`),
  KEY `IDX198` (`MODEL_NO`),
  KEY `IDX199` (`KEY_ID`),
  KEY `IDX200` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `I_COORD_DB`
--

DROP TABLE IF EXISTS `I_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `I_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX223` (`MODEL_NO`),
  KEY `IDX224` (`KEY_ID`),
  KEY `IDX225` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `I_CS_DB`
--

DROP TABLE IF EXISTS `I_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `I_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX226` (`ATOM_NAME`),
  KEY `IDX227` (`C_SHIFT`),
  KEY `IDX228` (`AMBIGUITY`),
  KEY `IDX229` (`KEY_ID`),
  KEY `IDX230` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `I_DB`
--

DROP TABLE IF EXISTS `I_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `I_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX231` (`CHAIN_ID`),
  KEY `IDX232` (`SEQ_ID`),
  KEY `IDX233` (`SEQ_NAME`),
  KEY `IDX234` (`KEY_ID`),
  KEY `IDX235` (`FIRSTKEY_ID`),
  KEY `IDX1018` (`PREV_X`),
  KEY `IDX1019` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `I_STRC_DB`
--

DROP TABLE IF EXISTS `I_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `I_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX214` (`SND_STRC`),
  KEY `IDX215` (`EDGE`),
  KEY `IDX216` (`PHI`),
  KEY `IDX217` (`PSI`),
  KEY `IDX218` (`HDO_PBT`),
  KEY `IDX219` (`SAS`),
  KEY `IDX220` (`MODEL_NO`),
  KEY `IDX221` (`KEY_ID`),
  KEY `IDX222` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `K_COORD_DB`
--

DROP TABLE IF EXISTS `K_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `K_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX267` (`MODEL_NO`),
  KEY `IDX268` (`KEY_ID`),
  KEY `IDX269` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `K_CS_DB`
--

DROP TABLE IF EXISTS `K_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `K_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX270` (`ATOM_NAME`),
  KEY `IDX271` (`C_SHIFT`),
  KEY `IDX272` (`AMBIGUITY`),
  KEY `IDX273` (`KEY_ID`),
  KEY `IDX274` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `K_DB`
--

DROP TABLE IF EXISTS `K_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `K_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX275` (`CHAIN_ID`),
  KEY `IDX276` (`SEQ_ID`),
  KEY `IDX277` (`SEQ_NAME`),
  KEY `IDX278` (`KEY_ID`),
  KEY `IDX279` (`FIRSTKEY_ID`),
  KEY `IDX1022` (`PREV_X`),
  KEY `IDX1023` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `K_STRC_DB`
--

DROP TABLE IF EXISTS `K_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `K_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX258` (`SND_STRC`),
  KEY `IDX259` (`EDGE`),
  KEY `IDX260` (`PHI`),
  KEY `IDX261` (`PSI`),
  KEY `IDX262` (`HDO_PBT`),
  KEY `IDX263` (`SAS`),
  KEY `IDX264` (`MODEL_NO`),
  KEY `IDX265` (`KEY_ID`),
  KEY `IDX266` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `L_COORD_DB`
--

DROP TABLE IF EXISTS `L_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `L_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX245` (`MODEL_NO`),
  KEY `IDX246` (`KEY_ID`),
  KEY `IDX247` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `L_CS_DB`
--

DROP TABLE IF EXISTS `L_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `L_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX248` (`ATOM_NAME`),
  KEY `IDX249` (`C_SHIFT`),
  KEY `IDX250` (`AMBIGUITY`),
  KEY `IDX251` (`KEY_ID`),
  KEY `IDX252` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `L_DB`
--

DROP TABLE IF EXISTS `L_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `L_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX253` (`CHAIN_ID`),
  KEY `IDX254` (`SEQ_ID`),
  KEY `IDX255` (`SEQ_NAME`),
  KEY `IDX256` (`KEY_ID`),
  KEY `IDX257` (`FIRSTKEY_ID`),
  KEY `IDX1020` (`PREV_X`),
  KEY `IDX1021` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `L_STRC_DB`
--

DROP TABLE IF EXISTS `L_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `L_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX236` (`SND_STRC`),
  KEY `IDX237` (`EDGE`),
  KEY `IDX238` (`PHI`),
  KEY `IDX239` (`PSI`),
  KEY `IDX240` (`HDO_PBT`),
  KEY `IDX241` (`SAS`),
  KEY `IDX242` (`MODEL_NO`),
  KEY `IDX243` (`KEY_ID`),
  KEY `IDX244` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `MOLPROB_DB`
--

DROP TABLE IF EXISTS `MOLPROB_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MOLPROB_DB` (
  `ID` int(11) default NULL,
  `PDB_ID` char(5) NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `CLASH_SCORE` double default NULL,
  `OUTLIER` double default NULL,
  `ALLOWED` double default NULL,
  `FAVORED` double default NULL,
  `BAD_BONDS` int(11) default NULL,
  `BAD_ANGLES` int(11) default NULL,
  `MOLPROB_SCORE` int(11) default NULL,
  `MOLPROB_RANK` int(11) default NULL,
  `KEY_ID` int(11) NOT NULL,
  KEY `IDX1` (`PDB_ID`),
  KEY `IDX2` (`MODEL_NO`),
  KEY `IDX3` (`CLASH_SCORE`),
  KEY `IDX4` (`OUTLIER`),
  KEY `IDX5` (`ALLOWED`),
  KEY `IDX6` (`FAVORED`),
  KEY `IDX7` (`BAD_BONDS`),
  KEY `IDX8` (`BAD_ANGLES`),
  KEY `IDX9` (`MOLPROB_SCORE`),
  KEY `IDX10` (`MOLPROB_RANK`),
  KEY `IDX11` (`KEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `M_COORD_DB`
--

DROP TABLE IF EXISTS `M_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `M_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX289` (`MODEL_NO`),
  KEY `IDX290` (`KEY_ID`),
  KEY `IDX291` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `M_CS_DB`
--

DROP TABLE IF EXISTS `M_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `M_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX292` (`ATOM_NAME`),
  KEY `IDX293` (`C_SHIFT`),
  KEY `IDX294` (`AMBIGUITY`),
  KEY `IDX295` (`KEY_ID`),
  KEY `IDX296` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `M_DB`
--

DROP TABLE IF EXISTS `M_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `M_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX297` (`CHAIN_ID`),
  KEY `IDX298` (`SEQ_ID`),
  KEY `IDX299` (`SEQ_NAME`),
  KEY `IDX300` (`KEY_ID`),
  KEY `IDX301` (`FIRSTKEY_ID`),
  KEY `IDX1024` (`PREV_X`),
  KEY `IDX1025` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `M_STRC_DB`
--

DROP TABLE IF EXISTS `M_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `M_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX280` (`SND_STRC`),
  KEY `IDX281` (`EDGE`),
  KEY `IDX282` (`PHI`),
  KEY `IDX283` (`PSI`),
  KEY `IDX284` (`HDO_PBT`),
  KEY `IDX285` (`SAS`),
  KEY `IDX286` (`MODEL_NO`),
  KEY `IDX287` (`KEY_ID`),
  KEY `IDX288` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `N_COORD_DB`
--

DROP TABLE IF EXISTS `N_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `N_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX69` (`MODEL_NO`),
  KEY `IDX70` (`KEY_ID`),
  KEY `IDX71` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `N_CS_DB`
--

DROP TABLE IF EXISTS `N_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `N_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX72` (`ATOM_NAME`),
  KEY `IDX73` (`C_SHIFT`),
  KEY `IDX74` (`AMBIGUITY`),
  KEY `IDX75` (`KEY_ID`),
  KEY `IDX76` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `N_DB`
--

DROP TABLE IF EXISTS `N_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `N_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX77` (`CHAIN_ID`),
  KEY `IDX78` (`SEQ_ID`),
  KEY `IDX79` (`SEQ_NAME`),
  KEY `IDX80` (`KEY_ID`),
  KEY `IDX81` (`FIRSTKEY_ID`),
  KEY `IDX1004` (`PREV_X`),
  KEY `IDX1005` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `N_STRC_DB`
--

DROP TABLE IF EXISTS `N_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `N_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX60` (`SND_STRC`),
  KEY `IDX61` (`EDGE`),
  KEY `IDX62` (`PHI`),
  KEY `IDX63` (`PSI`),
  KEY `IDX64` (`HDO_PBT`),
  KEY `IDX65` (`SAS`),
  KEY `IDX66` (`MODEL_NO`),
  KEY `IDX67` (`KEY_ID`),
  KEY `IDX68` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `P_COORD_DB`
--

DROP TABLE IF EXISTS `P_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `P_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX333` (`MODEL_NO`),
  KEY `IDX334` (`KEY_ID`),
  KEY `IDX335` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `P_CS_DB`
--

DROP TABLE IF EXISTS `P_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `P_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX336` (`ATOM_NAME`),
  KEY `IDX337` (`C_SHIFT`),
  KEY `IDX338` (`AMBIGUITY`),
  KEY `IDX339` (`KEY_ID`),
  KEY `IDX340` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `P_DB`
--

DROP TABLE IF EXISTS `P_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `P_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX341` (`CHAIN_ID`),
  KEY `IDX342` (`SEQ_ID`),
  KEY `IDX343` (`SEQ_NAME`),
  KEY `IDX344` (`KEY_ID`),
  KEY `IDX345` (`FIRSTKEY_ID`),
  KEY `IDX1028` (`PREV_X`),
  KEY `IDX1029` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `P_STRC_DB`
--

DROP TABLE IF EXISTS `P_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `P_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX324` (`SND_STRC`),
  KEY `IDX325` (`EDGE`),
  KEY `IDX326` (`PHI`),
  KEY `IDX327` (`PSI`),
  KEY `IDX328` (`HDO_PBT`),
  KEY `IDX329` (`SAS`),
  KEY `IDX330` (`MODEL_NO`),
  KEY `IDX331` (`KEY_ID`),
  KEY `IDX332` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Q_COORD_DB`
--

DROP TABLE IF EXISTS `Q_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Q_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX135` (`MODEL_NO`),
  KEY `IDX136` (`KEY_ID`),
  KEY `IDX137` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Q_CS_DB`
--

DROP TABLE IF EXISTS `Q_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Q_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX138` (`ATOM_NAME`),
  KEY `IDX139` (`C_SHIFT`),
  KEY `IDX140` (`AMBIGUITY`),
  KEY `IDX141` (`KEY_ID`),
  KEY `IDX142` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Q_DB`
--

DROP TABLE IF EXISTS `Q_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Q_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX143` (`CHAIN_ID`),
  KEY `IDX144` (`SEQ_ID`),
  KEY `IDX145` (`SEQ_NAME`),
  KEY `IDX146` (`KEY_ID`),
  KEY `IDX147` (`FIRSTKEY_ID`),
  KEY `IDX1010` (`PREV_X`),
  KEY `IDX1011` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Q_STRC_DB`
--

DROP TABLE IF EXISTS `Q_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Q_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX126` (`SND_STRC`),
  KEY `IDX127` (`EDGE`),
  KEY `IDX128` (`PHI`),
  KEY `IDX129` (`PSI`),
  KEY `IDX130` (`HDO_PBT`),
  KEY `IDX131` (`SAS`),
  KEY `IDX132` (`MODEL_NO`),
  KEY `IDX133` (`KEY_ID`),
  KEY `IDX134` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `R_COORD_DB`
--

DROP TABLE IF EXISTS `R_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `R_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX47` (`MODEL_NO`),
  KEY `IDX48` (`KEY_ID`),
  KEY `IDX49` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `R_CS_DB`
--

DROP TABLE IF EXISTS `R_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `R_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX50` (`ATOM_NAME`),
  KEY `IDX51` (`C_SHIFT`),
  KEY `IDX52` (`AMBIGUITY`),
  KEY `IDX53` (`KEY_ID`),
  KEY `IDX54` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `R_DB`
--

DROP TABLE IF EXISTS `R_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `R_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX55` (`CHAIN_ID`),
  KEY `IDX56` (`SEQ_ID`),
  KEY `IDX57` (`SEQ_NAME`),
  KEY `IDX58` (`KEY_ID`),
  KEY `IDX59` (`FIRSTKEY_ID`),
  KEY `IDX1002` (`PREV_X`),
  KEY `IDX1003` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `R_STRC_DB`
--

DROP TABLE IF EXISTS `R_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `R_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX38` (`SND_STRC`),
  KEY `IDX39` (`EDGE`),
  KEY `IDX40` (`PHI`),
  KEY `IDX41` (`PSI`),
  KEY `IDX42` (`HDO_PBT`),
  KEY `IDX43` (`SAS`),
  KEY `IDX44` (`MODEL_NO`),
  KEY `IDX45` (`KEY_ID`),
  KEY `IDX46` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `SCOP_DB`
--

DROP TABLE IF EXISTS `SCOP_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SCOP_DB` (
  `ID` int(11) default NULL,
  `ENTRY` char(8) NOT NULL,
  `DATA_TYPE` char(4) NOT NULL,
  `CLASS` char(1) default NULL,
  `FOLD` char(1) default NULL,
  `SUPERFAMILY` char(1) default NULL,
  `FAMILY` char(1) default NULL,
  `SCOP_ID` char(10) default NULL,
  `DESCRIPTION` text,
  `KEY_ID` int(11) NOT NULL,
  KEY `IDX10` (`DATA_TYPE`),
  KEY `IDX11` (`CLASS`),
  KEY `IDX12` (`FOLD`),
  KEY `IDX13` (`SUPERFAMILY`),
  KEY `IDX14` (`FAMILY`),
  KEY `IDX15` (`KEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `SEQ_DB`
--

DROP TABLE IF EXISTS `SEQ_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SEQ_DB` (
  `ID` int(11) default NULL,
  `PDB_ID` char(5) NOT NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `BMRB_ID` char(8) default NULL,
  `INIT_SEQ` int(11) NOT NULL,
  `SEQ_COUNT` int(11) NOT NULL,
  `CLASS` char(1) default NULL,
  `FOLD` char(1) default NULL,
  `SUPERFAMILY` char(1) default NULL,
  `FAMILY` char(1) default NULL,
  `SEQUENCE` text,
  `PH` double default NULL,
  `TEMP` double default NULL,
  `TITLE` text,
  `KEYWDS` text,
  `MODEL_COUNT` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  KEY `IDX1` (`PDB_ID`),
  KEY `IDX2` (`BMRB_ID`),
  KEY `IDX3` (`CHAIN_ID`),
  KEY `IDX4` (`SEQ_COUNT`),
  KEY `IDX5` (`CLASS`),
  KEY `IDX6` (`MODEL_COUNT`),
  KEY `IDX7` (`PH`),
  KEY `IDX8` (`TEMP`),
  KEY `IDX9` (`KEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `S_COORD_DB`
--

DROP TABLE IF EXISTS `S_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `S_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX355` (`MODEL_NO`),
  KEY `IDX356` (`KEY_ID`),
  KEY `IDX357` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `S_CS_DB`
--

DROP TABLE IF EXISTS `S_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `S_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX358` (`ATOM_NAME`),
  KEY `IDX359` (`C_SHIFT`),
  KEY `IDX360` (`AMBIGUITY`),
  KEY `IDX361` (`KEY_ID`),
  KEY `IDX362` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `S_DB`
--

DROP TABLE IF EXISTS `S_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `S_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX363` (`CHAIN_ID`),
  KEY `IDX364` (`SEQ_ID`),
  KEY `IDX365` (`SEQ_NAME`),
  KEY `IDX366` (`KEY_ID`),
  KEY `IDX367` (`FIRSTKEY_ID`),
  KEY `IDX1030` (`PREV_X`),
  KEY `IDX1031` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `S_STRC_DB`
--

DROP TABLE IF EXISTS `S_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `S_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX346` (`SND_STRC`),
  KEY `IDX347` (`EDGE`),
  KEY `IDX348` (`PHI`),
  KEY `IDX349` (`PSI`),
  KEY `IDX350` (`HDO_PBT`),
  KEY `IDX351` (`SAS`),
  KEY `IDX352` (`MODEL_NO`),
  KEY `IDX353` (`KEY_ID`),
  KEY `IDX354` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `T_COORD_DB`
--

DROP TABLE IF EXISTS `T_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX377` (`MODEL_NO`),
  KEY `IDX378` (`KEY_ID`),
  KEY `IDX379` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `T_CS_DB`
--

DROP TABLE IF EXISTS `T_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX380` (`ATOM_NAME`),
  KEY `IDX381` (`C_SHIFT`),
  KEY `IDX382` (`AMBIGUITY`),
  KEY `IDX383` (`KEY_ID`),
  KEY `IDX384` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `T_DB`
--

DROP TABLE IF EXISTS `T_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX385` (`CHAIN_ID`),
  KEY `IDX386` (`SEQ_ID`),
  KEY `IDX387` (`SEQ_NAME`),
  KEY `IDX388` (`KEY_ID`),
  KEY `IDX389` (`FIRSTKEY_ID`),
  KEY `IDX1032` (`PREV_X`),
  KEY `IDX1033` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `T_STRC_DB`
--

DROP TABLE IF EXISTS `T_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX368` (`SND_STRC`),
  KEY `IDX369` (`EDGE`),
  KEY `IDX370` (`PHI`),
  KEY `IDX371` (`PSI`),
  KEY `IDX372` (`HDO_PBT`),
  KEY `IDX373` (`SAS`),
  KEY `IDX374` (`MODEL_NO`),
  KEY `IDX375` (`KEY_ID`),
  KEY `IDX376` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `V_COORD_DB`
--

DROP TABLE IF EXISTS `V_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `V_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX443` (`MODEL_NO`),
  KEY `IDX444` (`KEY_ID`),
  KEY `IDX445` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `V_CS_DB`
--

DROP TABLE IF EXISTS `V_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `V_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX446` (`ATOM_NAME`),
  KEY `IDX447` (`C_SHIFT`),
  KEY `IDX448` (`AMBIGUITY`),
  KEY `IDX449` (`KEY_ID`),
  KEY `IDX450` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `V_DB`
--

DROP TABLE IF EXISTS `V_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `V_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX451` (`CHAIN_ID`),
  KEY `IDX452` (`SEQ_ID`),
  KEY `IDX453` (`SEQ_NAME`),
  KEY `IDX454` (`KEY_ID`),
  KEY `IDX455` (`FIRSTKEY_ID`),
  KEY `IDX1038` (`PREV_X`),
  KEY `IDX1039` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `V_STRC_DB`
--

DROP TABLE IF EXISTS `V_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `V_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX434` (`SND_STRC`),
  KEY `IDX435` (`EDGE`),
  KEY `IDX436` (`PHI`),
  KEY `IDX437` (`PSI`),
  KEY `IDX438` (`HDO_PBT`),
  KEY `IDX439` (`SAS`),
  KEY `IDX440` (`MODEL_NO`),
  KEY `IDX441` (`KEY_ID`),
  KEY `IDX442` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `W_COORD_DB`
--

DROP TABLE IF EXISTS `W_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `W_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX399` (`MODEL_NO`),
  KEY `IDX400` (`KEY_ID`),
  KEY `IDX401` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `W_CS_DB`
--

DROP TABLE IF EXISTS `W_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `W_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX402` (`ATOM_NAME`),
  KEY `IDX403` (`C_SHIFT`),
  KEY `IDX404` (`AMBIGUITY`),
  KEY `IDX405` (`KEY_ID`),
  KEY `IDX406` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `W_DB`
--

DROP TABLE IF EXISTS `W_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `W_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX407` (`CHAIN_ID`),
  KEY `IDX408` (`SEQ_ID`),
  KEY `IDX409` (`SEQ_NAME`),
  KEY `IDX410` (`KEY_ID`),
  KEY `IDX411` (`FIRSTKEY_ID`),
  KEY `IDX1034` (`PREV_X`),
  KEY `IDX1035` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `W_STRC_DB`
--

DROP TABLE IF EXISTS `W_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `W_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX390` (`SND_STRC`),
  KEY `IDX391` (`EDGE`),
  KEY `IDX392` (`PHI`),
  KEY `IDX393` (`PSI`),
  KEY `IDX394` (`HDO_PBT`),
  KEY `IDX395` (`SAS`),
  KEY `IDX396` (`MODEL_NO`),
  KEY `IDX397` (`KEY_ID`),
  KEY `IDX398` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `X_COORD_DB`
--

DROP TABLE IF EXISTS `X_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `X_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX465` (`MODEL_NO`),
  KEY `IDX466` (`KEY_ID`),
  KEY `IDX467` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `X_CS_DB`
--

DROP TABLE IF EXISTS `X_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `X_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX468` (`ATOM_NAME`),
  KEY `IDX469` (`C_SHIFT`),
  KEY `IDX470` (`AMBIGUITY`),
  KEY `IDX471` (`KEY_ID`),
  KEY `IDX472` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `X_DB`
--

DROP TABLE IF EXISTS `X_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `X_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX473` (`CHAIN_ID`),
  KEY `IDX474` (`SEQ_ID`),
  KEY `IDX475` (`SEQ_NAME`),
  KEY `IDX476` (`KEY_ID`),
  KEY `IDX477` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `X_STRC_DB`
--

DROP TABLE IF EXISTS `X_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `X_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX456` (`SND_STRC`),
  KEY `IDX457` (`EDGE`),
  KEY `IDX458` (`PHI`),
  KEY `IDX459` (`PSI`),
  KEY `IDX460` (`HDO_PBT`),
  KEY `IDX461` (`SAS`),
  KEY `IDX462` (`MODEL_NO`),
  KEY `IDX463` (`KEY_ID`),
  KEY `IDX464` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Y_COORD_DB`
--

DROP TABLE IF EXISTS `Y_COORD_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Y_COORD_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `X_COORD` double NOT NULL,
  `Y_COORD` double NOT NULL,
  `Z_COORD` double NOT NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX421` (`MODEL_NO`),
  KEY `IDX422` (`KEY_ID`),
  KEY `IDX423` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Y_CS_DB`
--

DROP TABLE IF EXISTS `Y_CS_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Y_CS_DB` (
  `ID` int(11) default NULL,
  `ATOM_NAME` char(6) NOT NULL,
  `C_SHIFT` double NOT NULL,
  `AMBIGUITY` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX424` (`ATOM_NAME`),
  KEY `IDX425` (`C_SHIFT`),
  KEY `IDX426` (`AMBIGUITY`),
  KEY `IDX427` (`KEY_ID`),
  KEY `IDX428` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Y_DB`
--

DROP TABLE IF EXISTS `Y_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Y_DB` (
  `ID` int(11) default NULL,
  `CHAIN_ID` char(1) NOT NULL,
  `SEQ_ID` int(11) NOT NULL,
  `SEQ_NAME` char(2) NOT NULL,
  `PREV_X` char(1) NOT NULL,
  `NEXT_X` char(1) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX429` (`CHAIN_ID`),
  KEY `IDX430` (`SEQ_ID`),
  KEY `IDX431` (`SEQ_NAME`),
  KEY `IDX432` (`KEY_ID`),
  KEY `IDX433` (`FIRSTKEY_ID`),
  KEY `IDX1036` (`PREV_X`),
  KEY `IDX1037` (`NEXT_X`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Y_STRC_DB`
--

DROP TABLE IF EXISTS `Y_STRC_DB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Y_STRC_DB` (
  `ID` int(11) default NULL,
  `SND_STRC` char(1) NOT NULL,
  `EDGE` char(1) NOT NULL,
  `PHI` double default NULL,
  `PSI` double default NULL,
  `HDO_PBT` double default NULL,
  `SAS` double default NULL,
  `MODEL_NO` int(11) NOT NULL,
  `KEY_ID` int(11) NOT NULL,
  `FIRSTKEY_ID` int(11) NOT NULL,
  KEY `IDX412` (`SND_STRC`),
  KEY `IDX413` (`EDGE`),
  KEY `IDX414` (`PHI`),
  KEY `IDX415` (`PSI`),
  KEY `IDX416` (`HDO_PBT`),
  KEY `IDX417` (`SAS`),
  KEY `IDX418` (`MODEL_NO`),
  KEY `IDX419` (`KEY_ID`),
  KEY `IDX420` (`FIRSTKEY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-11-28 16:22:37
