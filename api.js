// JavaScript Example: Reading Entities
// Filterable fields: code_input, error_message, programming_language, explanation_provided, solution_suggested, voice_used, session_duration, user_satisfaction, concepts_learned
async function fetchDebuggingSessionEntities() {
    const response = await fetch(`https://app.base44.com/api/apps/68b3fa2c4fa19b4df0e9470c/entities/DebuggingSession`, {
        headers: {
            'api_key': '8b824ca790ab4e108b94ef6ecbb26672', // or use await User.me() to get the API key
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    console.log(data);
}

// JavaScript Example: Updating an Entity
// Filterable fields: code_input, error_message, programming_language, explanation_provided, solution_suggested, voice_used, session_duration, user_satisfaction, concepts_learned
async function updateDebuggingSessionEntity(entityId, updateData) {
    const response = await fetch(`https://app.base44.com/api/apps/68b3fa2c4fa19b4df0e9470c/entities/DebuggingSession/${entityId}`, {
        method: 'PUT',
        headers: {
            'api_key': '8b824ca790ab4e108b94ef6ecbb26672', // or use await User.me() to get the API key
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateData)
    });
    const data = await response.json();
    console.log(data);
}