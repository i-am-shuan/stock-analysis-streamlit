import streamlit as st 
import stock_analysis_lib as glib 
import stock_analysis_database_lib as databaselib 
from langchain.callbacks import StreamlitCallbackHandler
from datetime import date
import pandas as pd
import plotly.graph_objects as go
import streamlit.components.v1 as components

def print_result(st, response):
    try:
        st.subheader("일별 주가:")
        st.dataframe(response['intermediate_steps'][1][1], use_container_width=True)
    except:
        print("Fail to draw price data table")

    try:
        st.subheader("주가 차트:")
        df = pd.DataFrame(response['intermediate_steps'][1][1], columns=['Close', 'Open', 'High', 'Low', 'Volume'])
        df['Volume'] = df['Volume']/5000000
        df.rename(columns={'Close': 'Close', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Volume': 'Volume(10 millions)'}, inplace=True)

        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA60'] = df['Close'].rolling(window=60).mean()

        fig = go.Figure()
        
        fig.add_trace(go.Candlestick(x=df.index,
                                    open=df['Open'],
                                    high=df['High'],
                                    low=df['Low'],
                                    close=df['Close'],
                                    name='Candlestick'))
        
        fig.add_trace(go.Scatter(x=df.index, y=df['MA5'], mode='lines', name='MA5'))
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], mode='lines', name='MA20'))
        fig.add_trace(go.Scatter(x=df.index, y=df['MA60'], mode='lines', name='MA60'))
        fig.add_trace(go.Bar(x=df.index, y=df['Volume(10 millions)'], name='Volume'))

        fig.update_layout(
            title=' ',
            xaxis_title='Date',
            yaxis_title='Price(USD)',
            yaxis2=dict(title='Volume(10 millions)', tickvals=df['Volume(10 millions)'], overlaying='y', side='right'),
            xaxis_rangeslider_visible=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig)
    except:
        print("Fail to draw price chart")
        
    try:
        st.subheader("재무 제표:")
        fs_df = pd.DataFrame(response['intermediate_steps'][3][1])
        fs_df.columns = pd.to_datetime(fs_df.columns, format='%Y-%m-%d').year
        st.dataframe(fs_df, use_container_width=True)
    except:
        print("Fail to draw financial statement")

    try:
        st.subheader("분석 결과:")
        st.write(response['output'])
    except:
        st.write(response['output'])

def stock_analysis():
    st.title("KB증권 GenAI Stock Agent")
    st.subheader("주식 분석을 위한 AI 투자 자문")
    st.write("Amazon, Tesla, Apple 등과 같은 회사명으로 입력해보세요 :)")

    if 'database' not in st.session_state: 
        with st.spinner("Initial Database"): 
            databaselib.initial_database() 
        
    if 'chat_history' not in st.session_state: 
        st.session_state.chat_history = [] 

    agent = glib.initializeAgent()
    
    # STT 컴포넌트
    st.write("음성으로 검색하시려면 마이크 버튼을 눌러주세요")
    components.html(
        """
        <div id="speech-container">
            <style>
                .mic-button {
                    background-color: transparent;
                    border: 2px solid #4B9CD3;
                    border-radius: 50%;
                    width: 50px;
                    height: 50px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 10px auto;
                    transition: all 0.3s ease;
                }
                .mic-button:hover {
                    background-color: rgba(75,156,211,0.1);
                }
                .mic-button.recording {
                    background-color: #4B9CD3;
                    animation: pulse 1.5s infinite;
                }
                .mic-button img {
                    width: 28px;
                    height: 28px;
                    filter: invert(45%) sepia(80%) saturate(400%) hue-rotate(165deg) brightness(90%) contrast(90%);
                }
                .mic-button.recording img {
                    filter: invert(100%);
                }
                @keyframes pulse {
                    0% { box-shadow: 0 0 0 0 rgba(75,156,211,0.4); }
                    70% { box-shadow: 0 0 0 15px rgba(75,156,211,0); }
                    100% { box-shadow: 0 0 0 0 rgba(75,156,211,0); }
                }
                #sttStatus {
                    text-align: center;
                    margin-top: 10px;
                    font-size: 14px;
                    min-height: 20px;
                }
                .recording-status {
                    color: #4B9CD3;
                    font-weight: 500;
                }
                .result-status {
                    color: #333;
                }
            </style>

            <button id="micButton" class="mic-button" title="음성 검색">
                <img src="https://cdnjs.cloudflare.com/ajax/libs/ionicons/5.5.2/collection/components/icon/svg/mic-outline.svg" alt="microphone"/>
            </button>
            <div id="sttStatus"></div>

            <script>
                let recognition;
                let isRecording = false;
                let lastTranscript = '';

                document.getElementById('micButton').addEventListener('click', function() {
                    if (!isRecording) {
                        startRecording();
                    } else {
                        stopRecording();
                    }
                });

                function updateInputAndSearch(text) {
                    const input = document.querySelector('input[data-testid="stTextInput"]');
                    if (input) {
                        input.value = text;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        
                        setTimeout(() => {
                            input.dispatchEvent(new KeyboardEvent('keydown', {
                                key: 'Enter',
                                code: 'Enter',
                                which: 13,
                                keyCode: 13,
                                bubbles: true
                            }));
                        }, 100);
                    }
                }

                function startRecording() {
                    if (!('webkitSpeechRecognition' in window)) {
                        alert('이 브라우저는 음성 인식을 지원하지 않습니다. Chrome 브라우저를 사용해주세요.');
                        return;
                    }

                    recognition = new webkitSpeechRecognition();
                    recognition.lang = 'ko-KR';
                    recognition.continuous = false;
                    recognition.interimResults = true;

                    recognition.onstart = function() {
                        isRecording = true;
                        document.getElementById('micButton').classList.add('recording');
                        document.getElementById('sttStatus').className = 'recording-status';
                        document.getElementById('sttStatus').textContent = '말씀해주세요...';
                        lastTranscript = '';
                    };

                    recognition.onend = function() {
                        isRecording = false;
                        document.getElementById('micButton').classList.remove('recording');
                        if (lastTranscript) {
                            document.getElementById('sttStatus').className = 'result-status';
                            document.getElementById('sttStatus').textContent = '검색어: ' + lastTranscript;
                        } else {
                            document.getElementById('sttStatus').textContent = '';
                        }
                    };

                    recognition.onresult = function(event) {
                        let interimTranscript = '';
                        let finalTranscript = '';

                        for (let i = event.resultIndex; i < event.results.length; i++) {
                            const transcript = event.results[i][0].transcript;
                            if (event.results[i].isFinal) {
                                finalTranscript = transcript;
                                lastTranscript = transcript;
                                updateInputAndSearch(transcript);
                                stopRecording();
                            } else {
                                interimTranscript = transcript;
                                document.getElementById('sttStatus').textContent = '인식 중: ' + transcript;
                            }
                        }
                    };

                    recognition.onerror = function(event) {
                        console.error('음성 인식 오류:', event.error);
                        document.getElementById('sttStatus').textContent = '음성 인식에 실패했습니다. 다시 시도해주세요.';
                        stopRecording();
                    };

                    recognition.start();
                }

                function stopRecording() {
                    if (recognition) {
                        recognition.stop();
                    }
                }
            </script>
        </div>
        """,
        height=100
    )
    
    # 입력 필드와 검색 결과 영역
    col1, col2 = st.columns([6, 1])
    
    with col1:
        input_text = st.text_input(
            "여기에 회사 이름 입력하세요!", 
            key="text_input"
        )

    # 검색 실행
    if input_text:
        with st.spinner("분석 중..."):
            st_callback = StreamlitCallbackHandler(st.container())
            response = agent({
                "input": input_text,
                "today": date.today(),
                "chat_history": st.session_state.chat_history,
            }, callbacks=[st_callback])
            
            print_result(st, response)

if __name__ == "__main__":
    stock_analysis()
