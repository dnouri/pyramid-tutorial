================
Pyramid Tutorial
================

About
=====

This is a repository containing all the examples and other material
used in the Pyramid tutorial held at EuroPython 2012 and Pycon DE
2012.

You can find out more about Pyramid here:

  http://www.pylonsproject.org

If you have questions about this tutorial, feel free to contact the
author at daniel.nouri@gmail.com


Installation
============

See INSTALL.txt for instructions on how to install the software
required to run the examples in this tutorial.


Examples
========

The example folders each contain a README.txt file with details on
what the example is about.  Here's a quick overview of all the
examples contained in this tutorial:

ex1_hello

  The first hello world application deals with basic views and
  configuration.

ex2_zodb_scaffold

  This example explains the various bits of code created by Pyramid's
  'zodb' scaffold.

ex3_templates

  In this step, we will implement our own first model, a 'Folder'.
  We will also split up our template, so that elements such as logo
  and navigation that appear in all our HTML pages, are separated out
  into a 'master template'.

ex4_forms

  In this part of the tutorial, we will add another model called
  'Page', so that then we're able to put pages into our folders.
  We'll also create HTML forms to be able to add, edit and delete
  folders and pages.

ex5_users

  In this part of the tutorial, we will add a 'User' model.  We'll
  also implement authentication, and allow new users to register with
  our site.

ex6_security

  In the final part of this tutorial, you will learn about security in
  Pyramid.  Concretely, you will guard your add and edit views with
  permissions, so that anonymous users can no longer edit any content.
  You will learn how to make use of Access Control Lists to allow
  users to edit content in their respective user folders.

ex7_final

  The last example project contains all the solutions for the
  ex6_security exercise.
