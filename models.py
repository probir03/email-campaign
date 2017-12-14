from flask import Flask, json, jsonify
from datetime import datetime, timedelta
from app import db
from sqlalchemy import text, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY, array
from helpers import datetime_to_epoch
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(100), primary_key=True)
    display_name = db.Column(db.String(70))
    first_name = db.Column(db.String(70))
    last_name = db.Column(db.String(70))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(60))
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    logo = db.Column(db.Text)
    credentials = db.Column(db.JSON)
    message_thread = db.Column(db.JSON)

    def transform(self):
        return {
            'id' : self.id,
            'displayName' : self.display_name,
            'firstName' : self.first_name,
            'lastName' : self.last_name,
            'email' : self.email,
            'logo' : self.logo
        }

class Drip(db.Model):
    __tablename__ = 'drips'

    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.ForeignKey(u'users.id', ondelete=u'CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    stage_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    recipient = db.Column(db.JSON, nullable=True)
    is_enabled = db.Column(db.Boolean, default=False)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())

    stages = relationship("Stage", backref="drip", order_by="asc(Stage.created_at)")
    user = relationship("User", backref="drips")

    @property
    def owner(self):
        return User.query.filter_by(id=self.user_id).first()
        
    @property
    def recipient_list(self):
        return self.recipient.split(', ')

    @property
    def letast_stage(self):
        return Stage.query.filter(Stage.drip_id==self.id).order_by('created_at').first()

    @property
    def running_stage(self):
        return Stage.query.filter(Stage.drip_id==self.id).order_by('created_at').first()

    @property
    def next_stage(self):
        return Stage.query.filter(Stage.drip_id==self.id, Stage.is_sent==False).order_by('created_at').first()

    def transform(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
        }

class Stage(db.Model):
    __tablename__ = 'stages'

    id = db.Column(db.String(100), primary_key=True)
    drip_id = db.Column(db.ForeignKey(u'drips.id', ondelete=u'CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.Text, nullable=False)
    template = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    variables = db.Column(db.JSON, default={})
    is_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def get_var(self, email, var):
        l_vars = self.get_vars(email) 
        if l_vars:
            return l_vars.get(var)
        return None

    def get_vars(self, email):
        if self.variables and email in self.variables:
            return self.variables[email]
        return None

    def list_vars(self):
        import re
        matches = re.findall(r"({{ *?\w+ *?}})", self.template)
        res = {}
        if matches:
            for match in matches:
                var_name = match.strip('{{').strip('}}').strip()
                res[var_name] = self.get_vars(var_name)
        return res

    def transform(self):
        return {
            'id' : self.id,
            'subjetc' : self.subjetc,
            'template' : self.template,
            'date' : self.date,
        }
