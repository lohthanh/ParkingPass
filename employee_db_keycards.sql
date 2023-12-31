-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema employee_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `employee_db` ;

-- -----------------------------------------------------
-- Schema employee_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `employee_db` DEFAULT CHARACTER SET utf8 ;
USE `employee_db` ;

-- -----------------------------------------------------
-- Table `employee_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `employee_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `password` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `employee_id` INT NULL,
  `user_level` TINYINT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `employee_db`.`keycards`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `employee_db`.`keycards` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `time` TIME NULL,
  `day_shift` TINYINT NULL,
  `evening_shift` TINYINT NULL,
  `graveyard_shift` TINYINT NULL,
  `swing_shift` TINYINT NULL,
  `price` DECIMAL NULL,
  `keycard_id` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_keycards_employees_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_keycards_employees`
    FOREIGN KEY (`user_id`)
    REFERENCES `employee_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
