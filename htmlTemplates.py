css = '''
<style>
body {
    background-color: #1a1a1a;
    color: #fff;
}

.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}

.chat-message.user {
    background-color: #9e9c91;
}

.chat-message.bot {
    background-color: #9c8136;
}

.chat-message .avatar {
    width: 20%;
    display: flex;
    align-items: flex-start;
    padding: 15px;
    border-radius: 20%;
    overflow: hidden;
}

.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    object-fit: cover;
}

.chat-message .message {
    width: 80%;
    padding: 1rem;
    font-size: 1.2rem;
}

/* Additional Styles for Improved Layout */

.chat-container {
    max-width: 600px;
    margin: 0 auto;
}
.buy-coffee-button {
    text-align: center;
    margin-top: 20px;
    margin-bottom: 20px;
}
}

.buy-coffee-button button {
    background-color: #ffffff;
    color: #fff;
    padding: 10px 20px;
    margin: 10 px;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
}

.coffee-emoji {
    font-size: 16px;
    margin-right: 5px;
}

</style>

'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://media.discordapp.net/attachments/1008571142858092684/1081722896805793902/WisdomBooze_Logo_of_a_golden_chess_king_glowing_with_a_black_ba_9ccff649-2b3a-4d71-ac20-dcb3c250ac4a.png?width=662&height=662" alt="Bot Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://media.discordapp.net/attachments/1008571074981658694/1136677460247855211/drinktab_Kangaroo_wearing_sunglasses_and_a_bowtie_minimalist_lo_34e02ac5-2711-41cc-ad94-d7053369064a.png?width=662&height=662">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''