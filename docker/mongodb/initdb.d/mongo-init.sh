#!/bin/bash
set -x #print out the statements as they are being executed
set -e #stop immediately if one of the statements it executes has an exit-code different from 0.

echo "***************************** Trying to insert Trailerplan users"
mongo --port 27017
mongo -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD<<EOF
use $MONGO_INITDB_DATABASE;
conn = new Mongo();
db = conn.getDB($MONGO_INITDB_DATABASE);
db.createCollection('p_user');

db.p_user.insert( { CIVILITE: 'Monsieur', FIRST_NAME: 'Kilian', LAST_NAME:'Jornet', SEXE:'masculin', BIRTHDAY:'1987-10-27', CITY:'Sabadell', COUNTRY:'Espagne'} );
db.p_user.insert( { CIVILITE: 'Monsieur', FIRST_NAME: 'Sebastien', LAST_NAME:'Chaigneau', SEXE:'masculin', BIRTHDAY:'1972-02-23', CITY:'Châtellerault', COUNTRY:'France'} );
db.p_user.insert( { CIVILITE: 'Madame', FIRST_NAME: 'Caroline', LAST_NAME:'Chaverot', SEXE:'féminin', BIRTHDAY:'1976-10-16', CITY:'Genève', COUNTRY:'Suisse'} );
db.p_user.insert( { CIVILITE: 'Monsieur', FIRST_NAME: 'Eric', LAST_NAME:'Clavery', SEXE:'masculin', BIRTHDAY:'1980-06-07', CITY:'Coutances', COUNTRY:'France'} );
db.p_user.insert( { CIVILITE: 'Monsieur', FIRST_NAME: 'François', LAST_NAME:'Delabarre', SEXE:'masculin', BIRTHDAY:'1968-01-03', CITY:'Lille', COUNTRY:'France'} );
db.p_user.insert( { CIVILITE: 'Madame', FIRST_NAME: 'Corinne', LAST_NAME:'Favre', SEXE:'féminin', BIRTHDAY:'1970-12-15', CITY:'Chambéry', COUNTRY:'France'} );
db.p_user.insert( { CIVILITE: 'Madame', FIRST_NAME: 'Emilie', LAST_NAME:'Forsberg', SEXE:'féminin', BIRTHDAY:'1986-12-11', CITY:'Sollefteå', COUNTRY:'Suède'} );
db.p_user.insert( { CIVILITE: 'Madame', FIRST_NAME: 'Anna', LAST_NAME:'Frost', SEXE:'féminin', BIRTHDAY:'1981-11-01', CITY:'Dunedin', COUNTRY:'Nouvelle-Zélande'} );
db.p_user.insert( { CIVILITE: 'Madame', FIRST_NAME: 'Maud', LAST_NAME:'Gobert', SEXE:'féminin', BIRTHDAY:'1977-04-25', CITY:'', COUNTRY:'France'} );
db.p_user.insert( { CIVILITE: 'Monsieur', FIRST_NAME: 'Antoine', LAST_NAME:'Guillon', SEXE:'masculin', BIRTHDAY:'1970-06-16', CITY:'Yvelines', COUNTRY:'France'} );
db.p_user.insert( { CIVILITE: 'Monsieur', FIRST_NAME: 'Scott', LAST_NAME:'Jurek', SEXE:'masculin', BIRTHDAY:'1973-10-26', CITY:'Duluth', COUNTRY:'Etats-Unis'} );
db.p_user.insert( { CIVILITE: 'Monsieur', FIRST_NAME: 'Anton', LAST_NAME:'Krupicka', SEXE:'masculin', BIRTHDAY:'1983-08-08', CITY:'Nebraska', COUNTRY:'Etats-Unis'} );
db.p_user.insert( { CIVILITE: 'Madame', FIRST_NAME: 'Nathalie', LAST_NAME:'Mauclair', SEXE:'féminin', BIRTHDAY:'1970-05-09', CITY:'', COUNTRY:'France'} );
db.p_user.insert( { CIVILITE: 'Monsieur', FIRST_NAME: 'Dawa', LAST_NAME:'Dachhiri Sherpa', SEXE:'masculin', BIRTHDAY:'1969-11-03', CITY:'Taksindu Solukumbu', COUNTRY:'Népal'} );
db.p_user.insert( { CIVILITE: 'Monsieur', FIRST_NAME: 'Xavier', LAST_NAME:'Thévenard', SEXE:'masculin', BIRTHDAY:'1988-03-06', CITY:'Nantua', COUNTRY:'France'} );
