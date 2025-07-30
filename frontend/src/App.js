// frontend/src/App.js (Версия для живого диалога с OpenAI)
// ... (весь остальной код такой же, как в версии с голосом и анализом) ...
// Ключевая часть - это функция handleUserResponse:

    const handleUserResponse = async (userText) => {
        if (isProcessing) return;
        setIsProcessing(true);

        const updatedConversation = [...conversation, { speaker: 'User', text: userText }];
        setConversation(updatedConversation);

        try {
            // Этот fetch отправляет диалог на бэкенд
            const response = await fetch(`${API_BASE_URL}/api/respond`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    conversation: updatedConversation,
                    scenario_id: scenario.id
                }),
            });
            const data = await response.json();

            // Здесь мы получаем настоящий ответ от OpenAI и озвучиваем его
            setConversation(prev => [...prev, { speaker: 'AI', text: data.ai_response }]);
            speakAIResponse(data.ai_response);

        } catch (error) {
            console.error("Failed to get AI response:", error);
            const errorText = 'Sorry, there was a connection issue.';
            setConversation(prev => [...prev, { speaker: 'AI', text: errorText }]);
            speakAIResponse(errorText);
        } finally {
            setIsProcessing(false);
        }
    };
// ... (остальной код App.js) ...
