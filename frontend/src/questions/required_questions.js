// ===============================
// REQUIRED QUESTIONS CONFIG FILE
// ===============================

export const optionARequired = [
    {
      id: "has_discovery_intent",
      type: "mc",
      label: "Do you have any idea what you want to do or what types of places you want to go?",
      options: ["Yes", "No"]
    },
    {
      id: "discovery_intent",
      type: "oe",
      label: "Describe the type(s) of places you want to go.",
      showIf: (formData) => formData.has_discovery_intent === "Yes"
    },
    {
      id: "knows_trip_length",
      type: "mc",
      label: "Do you know how long you want your trip to be?",
      options: ["Yes", "No"]
    },
    {
      id: "days",
      type: "num",
      label: "How long is your trip (in days)?",
      showIf: (formData) => formData.knows_trip_length === "Yes"
    },
    {
      id: "people",
      type: "mc",
      label: "How many people are planning to go?",
      options: ["1", "2", "3-4", "5-6", "7-9", "10-14", "15 or more"]
    },
    {
      id: "transport_mode",
      type: "mc",
      label: "How are you planning on getting to your destination?",
      options: ["Driving", "Flying", "Train", "Bus", "Cruise or ferry", "Not sure yet"]
    },
    {
      id: "origin_location",
      type: "oe",
      label: "Where are you currently? (City and country)"
    },
    {
      id: "international_travel",
      type: "mc",
      label: "Do you want to travel to a different country?",
      options: ["Yes", "No"]
    },
    {
      id: "preferred_countries",
      type: "oe",
      label: "What country (or countries) do you prefer?",
      showIf: (formData) => formData.international_travel === "Yes"
    },
    {
      id: "distance_preference",
      type: "mc",
      label: "How far do you want your destination to be?",
      options: [
        "<10 miles",
        "10-20 miles",
        "20-50 miles",
        "50-100 miles",
        "100-200 miles",
        "200-500 miles",
        ">500 miles"
      ],
      showIf: (formData) => formData.international_travel === "No"
    },
    {
      id: "has_dates",
      type: "mc",
      label: "Do you know the dates of your trip?",
      options: ["Yes", "No"]
    },
    {
      id: "date_range",
      type: "oe",
      label: "Enter dates in format: Month Day to Month Day",
      showIf: (formData) => formData.has_dates === "Yes"
    },
    {
      id: "has_time_constraints",
      type: "mc",
      label: "Are there any strict time constraints?",
      options: ["Yes", "No"]
    },
    {
      id: "time_constraints_detail",
      type: "oe",
      label: "Enter time constraints in format: Month Day from hh:mm AM/PM to hh:mm AM/PM",
      showIf: (formData) => formData.has_time_constraints === "Yes"
    },
    {
      id: "area_structure",
      type: "mc",
      label: "Are you planning to visit one area or multiple areas?",
      options: ["Yes", "No"]
    },
    {
      id: "special_group_needs",
      type: "cata",
      label: "Are you traveling with children, disabled people, or elderly people?",
      options: ["Children", "Disabled People", "Elderly People", "None"]
    },
    {
      id: "accessibility_needs",
      type: "mc",
      label: "Do you have mobility limitations or accessibility needs?",
      options: ["Yes", "No"]
    },
    {
      id: "accessibility_details",
      type: "oe",
      label: "Explain the mobility limitations or accessibility needs.",
      showIf: (formData) => formData.accessibility_needs === "Yes"
    }
  ];
  
  
  export const optionBRequired = [
    {
      id: "destination",
      type: "oe",
      label: "Where is your trip? Include dates if possible."
    },
    {
      id: "knows_trip_length_b",
      type: "mc",
      label: "Do you know how long your trip is?",
      options: ["Yes", "No"]
    },
    {
      id: "days_b",
      type: "num",
      label: "How long is your trip (in days)?",
      showIf: (formData) => formData.knows_trip_length_b === "Yes"
    },
    {
      id: "people_b",
      type: "mc",
      label: "How many people are planning to go?",
      options: ["1", "2", "3-4", "5-6", "7-9", "10-14", "15 or more"]
    },
    {
      id: "has_time_constraints",
      type: "mc",
      label: "Are there any strict time constraints?",
      options: ["Yes", "No"]
    },
    {
      id: "time_constraints_detail",
      type: "oe",
      label: "Enter time constraints in format: Month Day from hh:mm AM/PM to hh:mm AM/PM",
      showIf: (formData) => formData.has_time_constraints === "Yes"
    },
    {
      id: "special_group_needs",
      type: "cata",
      label: "Are you traveling with children, disabled people, or elderly people?",
      options: ["Children", "Disabled People", "Elderly People", "None"]
    },
    {
      id: "accessibility_needs",
      type: "mc",
      label: "Do you have mobility limitations or accessibility needs?",
      options: ["Yes", "No"]
    },
    {
      id: "accessibility_details",
      type: "oe",
      label: "Explain the mobility limitations or accessibility needs.",
      showIf: (formData) => formData.accessibility_needs === "Yes"
    }
  ];  