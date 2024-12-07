-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-12-2023 a las 20:26:23
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `coloquia`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumnos`
--

CREATE TABLE `alumnos` (
  `idAlumno` int(6) NOT NULL,
  `nombreAlumno` varchar(20) DEFAULT NULL,
  `apellidoAlumno` varchar(20) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencias`
--

CREATE TABLE `asistencias` (
  `idAsistencia` int(8) NOT NULL,
  `idCursada` int(5) DEFAULT NULL,
  `idAlumno` int(6) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `idScan` int(6) DEFAULT NULL,
  `idPresente` int(1) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cursadas`
--

CREATE TABLE `cursadas` (
  `idCursada` int(5) NOT NULL,
  `anio` int(4) DEFAULT NULL,
  `cuatrimestre` int(1) DEFAULT NULL,
  `dia` varchar(10) DEFAULT NULL,
  `idHoraInicio` int(2) DEFAULT NULL,
  `idHoraFin` int(2) DEFAULT NULL,
  `idProfesor` int(3) DEFAULT NULL,
  `idMateria` int(3) DEFAULT NULL,
  `idEscuela` int(3) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `escaneos`
--

CREATE TABLE `escaneos` (
  `idScan` int(6) NOT NULL,
  `hipervEscaneo` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `escuelas`
--

CREATE TABLE `escuelas` (
  `idEscuela` int(3) NOT NULL,
  `nombreEscuela` varchar(50) DEFAULT NULL,
  `idEstado` int(2) DEFAULT NULL,
  `idLocalidad` int(3) DEFAULT NULL,
  `calle` varchar(30) DEFAULT NULL,
  `numero` varchar(8) DEFAULT NULL,
  `codigoPostal` varchar(8) DEFAULT NULL,
  `telefono` varchar(16) DEFAULT NULL,
  `mail` varchar(50) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estados`
--

CREATE TABLE `estados` (
  `idEstado` int(2) NOT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horafin`
--

CREATE TABLE `horafin` (
  `idHoraFin` int(2) NOT NULL,
  `horaFin` time DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horainicio`
--

CREATE TABLE `horainicio` (
  `idHoraInicio` int(2) NOT NULL,
  `horaInicio` time DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `idpresentes`
--

CREATE TABLE `idpresentes` (
  `idPresente` int(1) NOT NULL,
  `descripcion` varchar(30) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inscripciones`
--

CREATE TABLE `inscripciones` (
  `idInscripcion` int(6) NOT NULL,
  `idCursada` int(5) DEFAULT NULL,
  `idAlumno` int(6) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `localidades`
--

CREATE TABLE `localidades` (
  `idLocalidad` int(3) NOT NULL,
  `localidad` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materiales`
--

CREATE TABLE `materiales` (
  `idMaterial` int(4) NOT NULL,
  `descripcion` varchar(50) DEFAULT NULL,
  `ubicacion` varchar(50) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materias`
--

CREATE TABLE `materias` (
  `idMateria` int(3) NOT NULL,
  `nombreMateria` varchar(50) DEFAULT NULL,
  `programa` varchar(50) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materiasmateriales`
--

CREATE TABLE `materiasmateriales` (
  `idMateriaMaterial` int(4) NOT NULL,
  `idMateria` int(3) DEFAULT NULL,
  `idMaterial` int(4) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materiasprofesores`
--

CREATE TABLE `materiasprofesores` (
  `idMateriaProf` int(4) NOT NULL,
  `idProfesor` int(3) DEFAULT NULL,
  `idMateria` int(3) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesores`
--

CREATE TABLE `profesores` (
  `idProfesor` int(3) NOT NULL,
  `nombreProfesor` varchar(30) DEFAULT NULL,
  `apellidoProfesor` varchar(30) DEFAULT NULL,
  `idEstado` int(2) DEFAULT NULL,
  `idLocalidad` int(3) DEFAULT NULL,
  `calle` varchar(30) DEFAULT NULL,
  `numero` varchar(8) DEFAULT NULL,
  `codigoPostal` varchar(8) DEFAULT NULL,
  `telefono` varchar(16) DEFAULT NULL,
  `mail` varchar(50) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `profesores`
--

INSERT INTO `profesores` (`idProfesor`, `nombreProfesor`, `apellidoProfesor`, `idEstado`, `idLocalidad`, `calle`, `numero`, `codigoPostal`, `telefono`, `mail`, `activo`) VALUES
(1, 'Amanda', 'Martinez', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarifaescuelas`
--

CREATE TABLE `tarifaescuelas` (
  `idTarifaEscuela` int(3) NOT NULL,
  `idEscuela` int(3) DEFAULT NULL,
  `idTarifa` int(2) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarifas`
--

CREATE TABLE `tarifas` (
  `idTarifa` int(2) NOT NULL,
  `tarifa` float(5,2) DEFAULT NULL,
  `materiales` float(4,2) DEFAULT NULL,
  `descripcion` varchar(50) DEFAULT NULL,
  `profesor` float(5,2) DEFAULT NULL,
  `coloquia` float(5,2) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD PRIMARY KEY (`idAlumno`);

--
-- Indices de la tabla `asistencias`
--
ALTER TABLE `asistencias`
  ADD PRIMARY KEY (`idAsistencia`),
  ADD KEY `idPresente` (`idPresente`),
  ADD KEY `idCursada` (`idCursada`),
  ADD KEY `idAlumno` (`idAlumno`),
  ADD KEY `idScan` (`idScan`);

--
-- Indices de la tabla `cursadas`
--
ALTER TABLE `cursadas`
  ADD PRIMARY KEY (`idCursada`),
  ADD KEY `idProfesor` (`idProfesor`),
  ADD KEY `idMateria` (`idMateria`),
  ADD KEY `idEscuela` (`idEscuela`),
  ADD KEY `idHoraInicio` (`idHoraInicio`),
  ADD KEY `idHoraFin` (`idHoraFin`);

--
-- Indices de la tabla `escaneos`
--
ALTER TABLE `escaneos`
  ADD PRIMARY KEY (`idScan`);

--
-- Indices de la tabla `escuelas`
--
ALTER TABLE `escuelas`
  ADD PRIMARY KEY (`idEscuela`),
  ADD KEY `idEstado` (`idEstado`),
  ADD KEY `idLocalidad` (`idLocalidad`);

--
-- Indices de la tabla `estados`
--
ALTER TABLE `estados`
  ADD PRIMARY KEY (`idEstado`);

--
-- Indices de la tabla `horafin`
--
ALTER TABLE `horafin`
  ADD PRIMARY KEY (`idHoraFin`);

--
-- Indices de la tabla `horainicio`
--
ALTER TABLE `horainicio`
  ADD PRIMARY KEY (`idHoraInicio`);

--
-- Indices de la tabla `idpresentes`
--
ALTER TABLE `idpresentes`
  ADD PRIMARY KEY (`idPresente`);

--
-- Indices de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD PRIMARY KEY (`idInscripcion`),
  ADD KEY `idCursada` (`idCursada`),
  ADD KEY `idAlumno` (`idAlumno`);

--
-- Indices de la tabla `localidades`
--
ALTER TABLE `localidades`
  ADD PRIMARY KEY (`idLocalidad`);

--
-- Indices de la tabla `materiales`
--
ALTER TABLE `materiales`
  ADD PRIMARY KEY (`idMaterial`);

--
-- Indices de la tabla `materias`
--
ALTER TABLE `materias`
  ADD PRIMARY KEY (`idMateria`);

--
-- Indices de la tabla `materiasmateriales`
--
ALTER TABLE `materiasmateriales`
  ADD PRIMARY KEY (`idMateriaMaterial`),
  ADD KEY `idMateria` (`idMateria`),
  ADD KEY `idMaterial` (`idMaterial`);

--
-- Indices de la tabla `materiasprofesores`
--
ALTER TABLE `materiasprofesores`
  ADD PRIMARY KEY (`idMateriaProf`),
  ADD KEY `idProfesor` (`idProfesor`),
  ADD KEY `idMateria` (`idMateria`);

--
-- Indices de la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD PRIMARY KEY (`idProfesor`),
  ADD KEY `idEstado` (`idEstado`),
  ADD KEY `idLocalidad` (`idLocalidad`);

--
-- Indices de la tabla `tarifaescuelas`
--
ALTER TABLE `tarifaescuelas`
  ADD PRIMARY KEY (`idTarifaEscuela`),
  ADD KEY `idEscuela` (`idEscuela`),
  ADD KEY `idTarifa` (`idTarifa`);

--
-- Indices de la tabla `tarifas`
--
ALTER TABLE `tarifas`
  ADD PRIMARY KEY (`idTarifa`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  MODIFY `idAlumno` int(6) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `asistencias`
--
ALTER TABLE `asistencias`
  MODIFY `idAsistencia` int(8) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cursadas`
--
ALTER TABLE `cursadas`
  MODIFY `idCursada` int(5) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `escaneos`
--
ALTER TABLE `escaneos`
  MODIFY `idScan` int(6) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `escuelas`
--
ALTER TABLE `escuelas`
  MODIFY `idEscuela` int(3) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `estados`
--
ALTER TABLE `estados`
  MODIFY `idEstado` int(2) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `horafin`
--
ALTER TABLE `horafin`
  MODIFY `idHoraFin` int(2) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `horainicio`
--
ALTER TABLE `horainicio`
  MODIFY `idHoraInicio` int(2) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `idpresentes`
--
ALTER TABLE `idpresentes`
  MODIFY `idPresente` int(1) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  MODIFY `idInscripcion` int(6) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `localidades`
--
ALTER TABLE `localidades`
  MODIFY `idLocalidad` int(3) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `materiales`
--
ALTER TABLE `materiales`
  MODIFY `idMaterial` int(4) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `materias`
--
ALTER TABLE `materias`
  MODIFY `idMateria` int(3) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `materiasmateriales`
--
ALTER TABLE `materiasmateriales`
  MODIFY `idMateriaMaterial` int(4) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `materiasprofesores`
--
ALTER TABLE `materiasprofesores`
  MODIFY `idMateriaProf` int(4) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `profesores`
--
ALTER TABLE `profesores`
  MODIFY `idProfesor` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `tarifaescuelas`
--
ALTER TABLE `tarifaescuelas`
  MODIFY `idTarifaEscuela` int(3) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tarifas`
--
ALTER TABLE `tarifas`
  MODIFY `idTarifa` int(2) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asistencias`
--
ALTER TABLE `asistencias`
  ADD CONSTRAINT `asistencias_ibfk_1` FOREIGN KEY (`idPresente`) REFERENCES `idpresentes` (`idPresente`),
  ADD CONSTRAINT `asistencias_ibfk_2` FOREIGN KEY (`idCursada`) REFERENCES `cursadas` (`idCursada`),
  ADD CONSTRAINT `asistencias_ibfk_3` FOREIGN KEY (`idAlumno`) REFERENCES `alumnos` (`idAlumno`),
  ADD CONSTRAINT `asistencias_ibfk_4` FOREIGN KEY (`idScan`) REFERENCES `escaneos` (`idScan`);

--
-- Filtros para la tabla `cursadas`
--
ALTER TABLE `cursadas`
  ADD CONSTRAINT `cursadas_ibfk_1` FOREIGN KEY (`idProfesor`) REFERENCES `profesores` (`idProfesor`),
  ADD CONSTRAINT `cursadas_ibfk_2` FOREIGN KEY (`idMateria`) REFERENCES `materias` (`idMateria`),
  ADD CONSTRAINT `cursadas_ibfk_3` FOREIGN KEY (`idEscuela`) REFERENCES `escuelas` (`idEscuela`),
  ADD CONSTRAINT `cursadas_ibfk_4` FOREIGN KEY (`idHoraInicio`) REFERENCES `horainicio` (`idHoraInicio`),
  ADD CONSTRAINT `cursadas_ibfk_5` FOREIGN KEY (`idHoraFin`) REFERENCES `horafin` (`idHoraFin`);

--
-- Filtros para la tabla `escuelas`
--
ALTER TABLE `escuelas`
  ADD CONSTRAINT `escuelas_ibfk_1` FOREIGN KEY (`idEstado`) REFERENCES `estados` (`idEstado`),
  ADD CONSTRAINT `escuelas_ibfk_2` FOREIGN KEY (`idLocalidad`) REFERENCES `localidades` (`idLocalidad`);

--
-- Filtros para la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD CONSTRAINT `inscripciones_ibfk_1` FOREIGN KEY (`idCursada`) REFERENCES `cursadas` (`idCursada`),
  ADD CONSTRAINT `inscripciones_ibfk_2` FOREIGN KEY (`idAlumno`) REFERENCES `alumnos` (`idAlumno`);

--
-- Filtros para la tabla `materiasmateriales`
--
ALTER TABLE `materiasmateriales`
  ADD CONSTRAINT `materiasmateriales_ibfk_1` FOREIGN KEY (`idMateria`) REFERENCES `materias` (`idMateria`),
  ADD CONSTRAINT `materiasmateriales_ibfk_2` FOREIGN KEY (`idMaterial`) REFERENCES `materiales` (`idMaterial`);

--
-- Filtros para la tabla `materiasprofesores`
--
ALTER TABLE `materiasprofesores`
  ADD CONSTRAINT `materiasprofesores_ibfk_1` FOREIGN KEY (`idProfesor`) REFERENCES `profesores` (`idProfesor`),
  ADD CONSTRAINT `materiasprofesores_ibfk_2` FOREIGN KEY (`idMateria`) REFERENCES `materias` (`idMateria`);

--
-- Filtros para la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD CONSTRAINT `profesores_ibfk_1` FOREIGN KEY (`idEstado`) REFERENCES `estados` (`idEstado`),
  ADD CONSTRAINT `profesores_ibfk_2` FOREIGN KEY (`idLocalidad`) REFERENCES `localidades` (`idLocalidad`);

--
-- Filtros para la tabla `tarifaescuelas`
--
ALTER TABLE `tarifaescuelas`
  ADD CONSTRAINT `tarifaescuelas_ibfk_1` FOREIGN KEY (`idEscuela`) REFERENCES `escuelas` (`idEscuela`),
  ADD CONSTRAINT `tarifaescuelas_ibfk_2` FOREIGN KEY (`idTarifa`) REFERENCES `tarifas` (`idTarifa`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
coloquia

update cursadas set fechaInicio = 2/13/24 where idCursada= 1
