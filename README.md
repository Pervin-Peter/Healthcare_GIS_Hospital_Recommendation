# AI-Based Healthcare Accessibility and Hospital Recommendation System using GIS

## Project Overview

This project develops a GIS-based healthcare accessibility and hospital recommendation system for Chennai.

It integrates hospital locations with nearby public transportation and healthcare-support facilities to calculate accessibility scores and recommend hospitals based on a selected patient location.

The system uses geospatial analysis, a weighted recommendation algorithm, Python, Flask, and an interactive Leaflet map.

## Objectives

* Visualize healthcare facilities across Chennai.
* Analyze proximity to bus stops, railway stations, clinics, and pharmacies.
* Calculate hospital accessibility scores.
* Recommend the Top 5 hospitals for a selected location.
* Display recommendation components through an interactive web application.

## Dataset Summary

| Dataset          |   Records |
| ---------------- | --------: |
| Hospitals        |       544 |
| Bus Stops        |       803 |
| Railway Stations |        93 |
| Clinics          |       358 |
| Pharmacies       |       221 |
| **Total**        | **2,019** |

## Technology Stack

* Python
* Flask
* Pandas
* GeoPandas
* QGIS
* Leaflet.js
* OpenStreetMap
* HTML, CSS, JavaScript
* Git and GitHub

## GIS Accessibility Scoring

The accessibility score considers:

| Facility         | Weight |
| ---------------- | -----: |
| Bus Stops        |    30% |
| Railway Stations |    20% |
| Clinics          |    20% |
| Pharmacies       |    30% |

Distance-to-score formula:

`Score = max(0, 100 × (1 − distance_km / 5))`

The 5 km threshold and weights are project-defined assumptions.

## Hospital Recommendation

The recommendation engine uses a weighted composite score:

| Component       | Weight |
| --------------- | -----: |
| Distance        |    30% |
| Specialty Match |    25% |
| Accessibility   |    25% |
| Emergency       |    10% |
| Healthcare Type |    10% |

The system displays the Top 5 recommended hospitals with component scores.

## Application Features

* Interactive Chennai map
* Toggleable GIS facility layers
* Patient location selection
* Medical specialty selection
* Hospital accessibility analysis
* Top 5 hospital recommendations
* Component-wise recommendation scores

## Project Architecture

Spatial Data → Data Preparation → GIS Accessibility Analysis → Hospital Recommendation Engine → Flask API → Leaflet Web Map

## Current Status

The working prototype supports facility visualization, patient-location selection, accessibility scoring, and hospital recommendations.

## Limitations

* Uses straight-line distance rather than road-network travel time.
* Scoring weights require further validation.
* Dataset completeness and freshness may vary.
* The current recommendation method is rule-based, not a trained ML model.

## Future Enhancements

* Road-network routing and travel-time analysis
* PostgreSQL/PostGIS integration
* Improved specialty and emergency-service data
* Validation using domain-expert feedback
* Enhanced visualization and deployment

## Academic Project

M.Tech – Artificial Intelligence
SRM Institute of Science and Technology

**Author:** Pervin Peter

---

This project is developed for academic and research purposes.
