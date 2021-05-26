-- ---------------------------------------------
-- Generated using MySQL dump
-- Server version: 5.7.33
-- Database: mlpipeline
-- ---------------------------------------------
-- $ brew install mysql-client
-- $ /usr/local/opt/mysql-client/bin/mysqldump mlpipeline --result-file=init_db.sql pipelines pipeline_versions --skip-add-drop-table --skip-disable-keys --skip-lock-tables --skip-add-locks --create-options --extended-insert --column-statistics=0 --user=root --host=169.45.121.104 --port=32259
-- ---------------------------------------------

CREATE TABLE IF NOT EXISTS `pipelines` (
  `UUID` varchar(255) NOT NULL,
  `CreatedAtInSec` bigint(20) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Description` longtext NOT NULL,
  `Parameters` longtext NOT NULL,
  `Status` varchar(255) NOT NULL,
  `DefaultVersionId` varchar(255) DEFAULT NULL,
  `Namespace` varchar(63) DEFAULT '',
  PRIMARY KEY (`UUID`),
  UNIQUE KEY `name_namespace_index` (`Name`,`Namespace`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `pipeline_versions` (
  `UUID` varchar(255) NOT NULL,
  `CreatedAtInSec` bigint(20) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Parameters` longtext NOT NULL,
  `PipelineId` varchar(255) NOT NULL,
  `Status` varchar(255) NOT NULL,
  `CodeSourceUrl` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`UUID`),
  UNIQUE KEY `idx_pipelineid_name` (`Name`,`PipelineId`),
  KEY `idx_pipeline_versions_CreatedAtInSec` (`CreatedAtInSec`),
  KEY `idx_pipeline_versions_PipelineId` (`PipelineId`),
  CONSTRAINT `pipeline_versions_PipelineId_pipelines_UUID_foreign` FOREIGN KEY (`PipelineId`) REFERENCES `pipelines` (`UUID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- don't populate tables since we won't have the accompanying "template" YAML stored on Minio
--

-- INSERT INTO `pipelines` VALUES ('c616527f-1f3c-4f0c-aada-35fa2cc4feb3',1619547888,'[Demo] flip-coin','[source code](https://github.com/kubeflow/kfp-tekton/tree/master/samples/flip-coin) A conditional pipeline to flip coins based on a random number generator.','[]','READY','c616527f-1f3c-4f0c-aada-35fa2cc4feb3','');
-- INSERT INTO `pipeline_versions` VALUES ('c616527f-1f3c-4f0c-aada-35fa2cc4feb3',1619547888,'[Demo] flip-coin','[]','c616527f-1f3c-4f0c-aada-35fa2cc4feb3','READY','');
