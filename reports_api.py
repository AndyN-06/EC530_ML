from flask import Flask, request, jsonify

def post_report():
    # post report
    return jsonify({"message": "Report posted successfully"}), 201

def get_report():
    # get report
    return jsonify({"report": "Report details"}), 200

def delete_report():
    # delete report
    return jsonify({"message": "Report deleted successfully"}), 200