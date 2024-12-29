import { roomService } from '../../../services/api/roomService.js';
import { LoadingSpinner } from '../../../components/LoadingSpinner.js';

export async function GameRoomsList() {
    const container = document.createElement('div');
    container.innerHTML = LoadingSpinner();

    try {
        const rooms = await roomService.getRooms();
        
        container.innerHTML = `
            <div class="card h-100">
                <div class="card-header bg-primary bg-gradient text-white d-flex justify-content-between align-items-center py-3">
                    <h5 class="mb-0">Active Game Rooms</h5>
                    <div class="d-flex gap-2">
                        <button class="btn btn-light btn-sm" id="refreshRooms">
                            <i class="bi bi-arrow-clockwise"></i>
                        </button>
                    </div>
                </div>
                <div class="card-body p-0">
                    <div class="list-group list-group-flush room-list" style="height: calc(100vh - 280px); overflow-y: auto;">
                        ${generateRoomsList(rooms)}
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        container.innerHTML = `
            <div class="alert alert-danger">
                Error loading rooms: ${error.message}
            </div>
        `;
    }

    return container.innerHTML;
}

function generateRoomsList(rooms) {
    if (!rooms.length) {
        return `
            <div class="list-group-item text-center text-muted py-5">
                No active rooms found
            </div>
        `;
    }

    return rooms.map(room => `
        <div class="list-group-item list-group-item-action p-3" data-room-id="${room.id}">
            <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                    <div class="room-icon me-3 p-2 bg-${getBadgeColor(room.type)} bg-opacity-10 rounded-circle">
                        <i class="bi bi-controller fs-4 text-${getBadgeColor(room.type)}"></i>
                    </div>
                    <div>
                        <h6 class="mb-1">${room.name}</h6>
                        <small class="text-muted">Hosted by ${room.host}</small>
                    </div>
                </div>
                <div class="d-flex align-items-center gap-3">
                    <div class="text-end">
                        <span class="badge bg-${getBadgeColor(room.type)}">${room.type}</span>
                        <small class="d-block text-muted mt-1">${room.skill || 'All Levels'}</small>
                    </div>
                    <div class="text-end">
                        <div class="mb-1">${room.players.length}/${room.maxPlayers}</div>
                        <small class="text-muted">${room.status}</small>
                    </div>
                    <a href="#/game-room" >
                    <button class="btn btn-primary btn-sm join-room-btn">
                        ${room.status === "Waiting" ? "Join" : "Spectate"}
                    </button>
                    </a>
                </div>
            </div>
        </div>
    `).join('');
}

function getBadgeColor(type) {
    const colors = {
        'Ranked': 'danger',
        'Casual': 'success',
        'Tournament': 'warning'
    };
    return colors[type] || 'primary';
}