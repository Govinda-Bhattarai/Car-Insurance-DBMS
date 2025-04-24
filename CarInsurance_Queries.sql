
-- -----------------------------------------------------
-- Schema CarInsurance
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `CarInsurance`;
USE `CarInsurance` ;

-- -----------------------------------------------------
-- Table `CarInsurance`.`owner`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `owner` (
  `owner_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `address` VARCHAR(255) NULL,
  `phone` VARCHAR(20) NULL,
  PRIMARY KEY (`owner_id`));


-- -----------------------------------------------------
-- Table `CarInsurance`.`car`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `car` (
  `engine_no` VARCHAR(50) NOT NULL,
  `owner_id` INT NOT NULL,
  `make` VARCHAR(100) NULL,
  `model` VARCHAR(100) NULL,
  `year` DATE NULL,
  `chassis_no` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`engine_no`),
  CONSTRAINT `owner_id`
    FOREIGN KEY (`owner_id`)
    REFERENCES `CarInsurance`.`owner` (`owner_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table `CarInsurance`.`policy`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `policy` (
  `policy_id` INT NOT NULL AUTO_INCREMENT,
  `car_id` VARCHAR(50) NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE GENERATED ALWAYS AS (adddate(start_date, INTERVAL 1 YEAR)),
  PRIMARY KEY (`policy_id`),
  CONSTRAINT `car_id`
    FOREIGN KEY (`car_id`)
    REFERENCES `car` (`engine_no`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table `CarInsurance`.`workshop`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `workshop` (
  `workshop_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `address` VARCHAR(255) NULL,
  `phone` VARCHAR(20) NULL,
  PRIMARY KEY (`workshop_id`));

-- -----------------------------------------------------
-- Table `CarInsurance`.`claim`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `claim` (
  `claim_id` INT NOT NULL AUTO_INCREMENT,
  `policy_no` INT NOT NULL,
  `claim_date` DATE NULL,
  `workshop_id` INT NULL,
  `driver_name` VARCHAR(255) NULL,
  `driver_license_no` VARCHAR(45) NULL,
  `status` VARCHAR(40), -- PROCESSING PAID
  `claim_amt` DOUBLE NULL,
  PRIMARY KEY (`claim_id`),
  CONSTRAINT `policy_no`
    FOREIGN KEY (`policy_no`)
    REFERENCES `policy` (`policy_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `workshop_id`
    FOREIGN KEY (`workshop_id`)
    REFERENCES `workshop` (`workshop_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
